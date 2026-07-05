# commission-worker — the $5.99 request box

Turns a Stripe Payment Link into GitHub issues labeled `commission`, which the
foundry's shift intake queues onto the roadmap. ~100 lines, free tiers throughout,
zero secrets in the repo.

## Flow
Stripe Payment Link (price + one custom text field) → `checkout.session.completed`
webhook → this Worker verifies the signature → opens the issue → `tools/intake.py`
queues it next shift → LOOP.md priority 3 builds it → publish closes the issue with
the install command.

## Setup (~15 minutes)
1. **Stripe** (dashboard):
   - Create a Product ("Plugin commission", $5.99 or your price).
   - Create a **Payment Link** for it. Add a required **custom text field** with key
     `plugin_request`, label "Describe the plugin you want".
   - In the link's description, keep the promise honest — suggested copy:
     "Buys a priority slot on the workshop's roadmap and a serious attempt at the
     full quality bar — not a guaranteed delivery. You'll receive the public GitHub
     issue where every stage of the work is commented."
   - Paste the link URL into `foundry/site-config.json` → `stripe_payment_link`.
2. **GitHub**: create a fine-grained PAT scoped to the foundry repo, permission
   Issues: Read & write only.
3. **Cloudflare**: `npm i -g wrangler && wrangler login`, then from this directory:
   ```bash
   wrangler deploy worker.js --name foundry-commissions
   wrangler secret put STRIPE_WEBHOOK_SECRET   # created in step 4, circle back
   wrangler secret put GITHUB_TOKEN
   wrangler secret put GITHUB_REPO             # e.g. yourname/pluginfoundry
   ```
4. **Stripe webhook**: add an endpoint pointing at the Worker URL, subscribed to
   `checkout.session.completed`; copy its signing secret into step 3.
5. Test with Stripe's "send test event" — an issue should appear within seconds.

## Operator responsibilities (the loop can't own these)
Payments, refunds, disputes, and taxes are yours, via the Stripe dashboard — decide
a refund policy (e.g., full refund if a commission is shelved) and say it on the
payment link. The Worker stores nothing; the issue carries only the request text and
a session id for your reconciliation.
