# Plausible Analytics Goals to Set Up

Log in to https://plausible.io/toolforge-io.netlify.app/settings/goals

## Goals to add (click "Add goal" for each):

1. **Affiliate Click (Jasper)**
   - Event name: `affiliate_click`
   - Trigger: `click` on elements matching `a[href*="jasper.ai"]`

2. **Affiliate Click (Cursor)**
   - Event name: `affiliate_click`
   - Trigger: `click` on elements matching `a[href*="cursor.com"]`

3. **Affiliate Click (ElevenLabs)**
   - Event name: `affiliate_click`
   - Trigger: `click` on elements matching `a[href*="elevenlabs.io"]`

4. **Sponsored Page View**
   - Event name: `view_sponsored_pricing`
   - Trigger: `pageview` on `/sponsored.html`

5. **Submit Tool Form**
   - Event name: `submit_tool_inquiry`
   - Trigger: `form_submit` on `form[action*="formspree"]`

6. **Newsletter Signup**
   - Event name: `newsletter_signup`
   - Trigger: `form_submit` on `form[action*="formspree"]`

7. **Deals Page CTA Click**
   - Event name: `deals_cta_click`
   - Trigger: `click` on `a[href^="https://"][href*="via=toolforge"]` on /deals.html

## Funnel to track:
1. Visitor lands on /deals.html
2. Clicks an affiliate link
3. (Conversion tracked on affiliate network's side)

## Custom properties to add (Settings > Properties):
- `audience` — set per page (e.g., "freelancers" on freelancer page)
- `category` — set per page (e.g., "writing" on writing category)
