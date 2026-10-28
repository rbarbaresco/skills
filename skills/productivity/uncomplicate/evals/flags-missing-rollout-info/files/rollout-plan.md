# Checkout v2 rollout plan

We are moving all web traffic from the current checkout to Checkout v2 over three weeks, starting on June 3.

## Stages

- Week 1: 5% of traffic, web only.
- Week 2: 25% of traffic, if the error rate stays under the threshold.
- Week 3: 100% of traffic.

As the numbers above show, v2 is faster and converts better, so we don't expect problems at 25%.

## If something goes wrong

If the error rate goes over the threshold at any stage, the on-call engineer follows the rollback procedure in section 4 and posts in #checkout-launch.

## Owners

Payments team owns the rollout. The go/no-go decision for week 3 is made by TBD.
