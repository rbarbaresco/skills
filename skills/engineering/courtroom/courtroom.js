export const meta = {
  name: 'courtroom',
  description: 'Adversarial ruling on a motion: detectives gather evidence, prosecutor argues for the motion, defense against, specialist jury votes, judge rules — extra hearing rounds when needed',
  whenToUse: 'Deciding whether to grant a proposed action (fix, approve, proceed, roll back, defer). Run through the /courtroom skill.',
  phases: [
    { title: 'Investigation', detail: 'four detectives, one angle each' },
    { title: 'Prosecution', detail: 'grounds for the motion, built from the evidence' },
    { title: 'Defense', detail: 'rebuttals; own investigation if requested' },
    { title: 'Jury', detail: 'one vote per seat' },
    { title: 'Judgment', detail: 'ruling on the motion, or requests for more information' },
  ],
}

// ---- inputs -------------------------------------------------------------

const CASE = args.case
const MOTION = args.motion
const CONTEXT = args.context || ''
const SEATS = (args.jury && args.jury.length)
  ? args.jury
  : ['security', 'backend (the stack in the case)', 'API/HTTP contract', 'SRE/observability', 'business/product impact']
const MAX_ROUNDS = args.maxRounds || 3

const RULINGS = ['granted', 'granted-in-part', 'denied']
const CONFIDENCE = ['low', 'medium', 'high']

// ---- schemas ------------------------------------------------------------

const EVIDENCE = {
  type: 'object',
  required: ['facts'],
  properties: {
    facts: {
      type: 'array',
      items: {
        type: 'object',
        required: ['claim', 'source', 'confidence'],
        properties: {
          claim: { type: 'string' },
          source: { type: 'string', description: 'file:line, monitor/SLO id, error-tracker issue, PR number, ticket key, query — something a reader can open' },
          confidence: { type: 'string', enum: CONFIDENCE },
        },
      },
    },
    gaps: { type: 'array', items: { type: 'string' }, description: 'what you looked for and could not find; omit or send [] when there are none' },
  },
}

const GROUNDS = {
  type: 'object',
  required: ['thesis', 'grounds', 'requested_ruling', 'requested_remedy'],
  properties: {
    thesis: { type: 'string', description: 'one paragraph, plain language: your overall theory of why the motion should be granted — what the facts show and why they matter — before the itemized grounds' },
    grounds: {
      type: 'array',
      items: {
        type: 'object',
        required: ['claim', 'weight', 'evidence'],
        properties: {
          claim: { type: 'string' },
          weight: { type: 'string', enum: ['low', 'medium', 'high'], description: 'how much of the motion this ground alone carries' },
          evidence: { type: 'string', description: 'which facts from the record support this, by source' },
        },
      },
    },
    requested_ruling: { type: 'string', enum: RULINGS },
    requested_remedy: { type: 'string', description: 'what the court should order, one or two sentences: the motion as filed, or the strongest version your grounds honestly carry' },
    open_questions: { type: 'array', items: { type: 'string' }, description: 'omit or send [] when there are none' },
  },
}

const DEFENSE = {
  type: 'object',
  required: ['thesis', 'rebuttals', 'requested_ruling', 'requested_remedy'],
  properties: {
    thesis: { type: 'string', description: 'one paragraph, plain language: your overall counter-theory — why the motion should be denied or narrowed compared to the grounds — before the itemized rebuttals' },
    rebuttals: {
      type: 'array',
      items: {
        type: 'object',
        required: ['ground', 'counter', 'evidence'],
        properties: {
          ground: { type: 'string' },
          counter: { type: 'string' },
          evidence: { type: 'string' },
        },
      },
    },
    requested_ruling: { type: 'string', enum: RULINGS },
    requested_remedy: { type: 'string', description: 'what the court should order instead, one or two sentences: the least your rebuttals honestly carry — a narrower action, or nothing' },
    investigation_requests: {
      type: 'array',
      items: { type: 'string' },
      description: 'specific questions you want detectives to answer before you finalize; omit or send [] if none',
    },
  },
}

const VOTE = {
  type: 'object',
  required: ['seat', 'ruling', 'remedy', 'confidence', 'reasoning'],
  properties: {
    seat: { type: 'string' },
    ruling: { type: 'string', enum: RULINGS, description: 'on the motion as filed' },
    remedy: { type: 'string', description: 'what your specialty says the operator should do; for granted-in-part, the narrower action' },
    confidence: { type: 'string', enum: CONFIDENCE },
    reasoning: { type: 'string', description: 'one plain-language paragraph from your specialty' },
    unanswered_questions: { type: 'array', items: { type: 'string' }, description: 'omit or send [] when you have none' },
  },
}

const JUDGMENT = {
  type: 'object',
  required: ['ready'],
  properties: {
    ready: { type: 'boolean', description: 'true when you can rule now' },
    ruling: {
      type: 'object',
      required: ['decision', 'remedy', 'confidence', 'reasoning', 'dissent'],
      properties: {
        decision: { type: 'string', enum: RULINGS, description: 'on the motion as filed' },
        remedy: { type: 'string', description: 'the order, one or two sentences: what the operator should do; for denied, what to do instead (including nothing, or refile after X)' },
        confidence: { type: 'string', enum: CONFIDENCE },
        reasoning: { type: 'string', description: 'plain language; if the case splits into separate findings, rule on each one explicitly' },
        dissent: { type: 'string', description: 'which seats disagreed and why; what stayed unresolved' },
      },
    },
    requests: {
      type: 'array',
      items: {
        type: 'object',
        required: ['to', 'question'],
        properties: {
          to: { type: 'string', enum: ['detectives', 'prosecutor', 'defense'] },
          question: { type: 'string' },
        },
      },
      description: 'omit or send [] when ready is true',
    },
  },
}

// ---- record -------------------------------------------------------------

const fmt = (o) => JSON.stringify(o, null, 2)
const evidence = []
let grounds = null
let defense = null
let votes = []
const judgments = []

const header = () => `CASE ON TRIAL:\n${CASE}\n\nMOTION SOUGHT:\n${MOTION}\n${CONTEXT ? `\nOPERATOR CONTEXT:\n${CONTEXT}\n` : ''}`
const record = () => fmt({ evidence, grounds, defense, votes, judgments })

// ---- helpers ------------------------------------------------------------

async function investigate(assignments, phaseName) {
  const results = await parallel(assignments.map(([label, brief]) => () =>
    agent(
      `${header()}\nYOUR ASSIGNMENT: ${brief}\n\nEVIDENCE ALREADY ON FILE (extend it, don't repeat it):\n${fmt(evidence)}`,
      { agentType: 'rbarbaresco-skills:courtroom-detective', schema: EVIDENCE, label: `detective:${label}`, phase: phaseName },
    )))
  results.forEach((r, i) => {
    if (r) evidence.push({ assignment: assignments[i][1], ...r, gaps: r.gaps || [] })
    else log(`detective:${assignments[i][0]} returned nothing — gap in the record`)
  })
}

const prosecute = (extra, phaseName) => agent(
  `${header()}\n${extra}\n\nFULL RECORD:\n${record()}\n\nReturn your complete, updated set of grounds — all of them, not only new ones.`,
  { agentType: 'rbarbaresco-skills:courtroom-prosecutor', schema: GROUNDS, phase: phaseName },
).then((c) => c && { ...c, open_questions: c.open_questions || [] })

const defend = (extra, phaseName) => agent(
  `${header()}\n${extra}\n\nFULL RECORD:\n${record()}\n\nReturn your complete, updated rebuttals — all of them, not only new ones.`,
  { agentType: 'rbarbaresco-skills:courtroom-defense', schema: DEFENSE, phase: phaseName },
).then((d) => d && { ...d, investigation_requests: d.investigation_requests || [] })

// ---- trial --------------------------------------------------------------

phase('Investigation')
await investigate([
  ['code', 'the code and its history: where it lives, what it does, who wrote it and why (git log/blame, PR descriptions, linked tickets), and what changed recently'],
  ['observability', 'production behaviour: monitors, SLOs, traces, logs and error-tracker issues from whatever monitoring tools this session can reach — volumes, error rates, latency, since when, trend, best and worst periods'],
  ['usage', 'who depends on it: callers in other repositories (gh code search across the repositories you can access), data-warehouse usage, which user personas it serves and how often'],
  ['organization', 'what people already know: tickets, docs and wiki pages, chat threads, past incidents and decisions about it'],
], 'Investigation')
log(`Investigation: ${evidence.reduce((n, e) => n + e.facts.length, 0)} facts, ${evidence.reduce((n, e) => n + e.gaps.length, 0)} gaps`)

phase('Prosecution')
grounds = await prosecute('Argue that the motion should be granted, from the evidence on file.', 'Prosecution')
if (!grounds) { log('Prosecutor returned nothing — trial cannot continue'); return { ruling: null, unresolved: ['prosecutor returned nothing'], evidence } }

phase('Defense')
defense = await defend('Answer the grounds. If you need facts the record lacks, list them in investigation_requests.', 'Defense')
if (defense && defense.investigation_requests.length) {
  log(`Defense requested ${defense.investigation_requests.length} investigation(s)`)
  await investigate(defense.investigation_requests.map((q, i) => [`defense-${i + 1}`, q]), 'Defense')
  defense = await defend('Your requested investigations are now in the record. Finalize your rebuttals; leave investigation_requests empty.', 'Defense')
}

let round = 0
let judgment = null
while (true) {
  round++
  phase('Jury')
  votes = (await parallel(SEATS.map((seat) => () => agent(
    `${header()}\nYou hold the "${seat}" seat. Vote only from that specialty's point of view.\n\nFULL RECORD:\n${record()}`,
    { agentType: 'rbarbaresco-skills:courtroom-juror', schema: VOTE, label: `juror:${seat}`, phase: 'Jury' },
  ).then((v) => v && { ...v, unanswered_questions: v.unanswered_questions || [] })))).filter(Boolean)
  if (votes.length < SEATS.length) log(`Jury: ${SEATS.length - votes.length} seat(s) returned nothing`)

  phase('Judgment')
  const last = round >= MAX_ROUNDS
  const openQuestions = votes.flatMap((v) => v.unanswered_questions || []).length
  const openGaps = evidence.flatMap((e) => e.gaps || []).length
  const belowHigh = votes.filter((v) => v.confidence !== 'high').length
  const digest = `SIGNAL DIGEST: ${openQuestions} unanswered juror question(s) across ${votes.length} vote(s), ${openGaps} evidence gap(s) on file, ${belowHigh} juror(s) below high confidence.`
  judgment = await agent(
    `${header()}\nHearing round ${round} of ${MAX_ROUNDS}.${last ? ' This is the last round: you MUST rule now (ready=true) and name anything still unresolved in the dissent field.' : ' If the record is enough, rule now. If not, ask precise questions in requests and set ready=false.'}\n${digest}\n\nFULL RECORD:\n${record()}`,
    { agentType: 'rbarbaresco-skills:courtroom-judge', schema: JUDGMENT, phase: 'Judgment' },
  )
  if (judgment) judgment.requests = judgment.requests || []
  judgments.push({ round, ...(judgment || { ready: false, requests: [], error: 'judge returned nothing' }) })
  if (!judgment || judgment.ready || last) break

  log(`Round ${round}: judge asked ${judgment.requests.length} follow-up question(s)`)
  const toDetectives = judgment.requests.filter((r) => r.to === 'detectives')
  const toParties = judgment.requests.filter((r) => r.to !== 'detectives')
  const hearing = `Hearing ${round}`
  await parallel([
    () => toDetectives.length
      ? investigate(toDetectives.map((r, i) => [`judge-r${round}-${i + 1}`, r.question]), hearing)
      : null,
    ...toParties.map((r) => () => (r.to === 'prosecutor'
      ? prosecute(`The judge asks you: ${r.question}`, hearing).then((c) => { if (c) grounds = c })
      : defend(`The judge asks you: ${r.question}`, hearing).then((d) => { if (d) defense = d }))),
  ])
}

const ruling = judgment && judgment.ruling ? judgment.ruling : null
if (!ruling) log('No ruling was produced — see judgments for what the judge asked')

return {
  ruling,
  rounds: round,
  seats: SEATS,
  votes,
  grounds,
  defense,
  evidence,
  judgments,
  unresolved: judgment ? judgment.requests : ['judge returned nothing'],
}
