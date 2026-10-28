# Public API rate limiting

## Behaviour

Each key gets a bucket of 20 tokens that refills at 100 tokens per minute; a request consumes one token and is rejected when the bucket is empty, with a 429 and a Retry-After header giving the number of seconds until one token is available. Limits apply per key, not per IP, so several clients behind one NAT do not share a limit, but one key used from many machines does. Keys of type internal are exempt. The refill is continuous, not per minute boundary, so a key that is idle for 12 seconds has 20 tokens again.

## Why

Last quarter three customers' batch jobs caused p99 latency on the public API to exceed 2 seconds for everyone (incidents INC-2207, INC-2231, INC-2240). A fixed window was considered but rejected because it allows 2x the limit across a window boundary.

## Terms

A key is an API key as issued in the dashboard; each has a type, either standard or internal. A token bucket is a counter that refills at a fixed rate up to a maximum (the burst size, here 20) and is decremented by each request. Retry-After is the standard HTTP header (RFC 9110, section 10.2.3).

## Rollout

Shadow mode first: we log what would have been rejected for two weeks without rejecting. Then enforce for standard keys. Customers above 80% of the limit in shadow mode get an email at least 7 days before enforcement.

## Open items

Whether the dashboard should show current usage is not decided. Limits for websocket connections are out of scope for this spec.
