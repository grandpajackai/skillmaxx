# Analytics recommendation

The site currently has **no analytics**, so the sponsor kit can't quote traffic yet.

| Option | Cost | Cookies / consent banner | Account | Notes |
|---|---|---|---|---|
| **Cloudflare Web Analytics** | Free, commercial use OK | No cookies, no banner | Cloudflare account | One `<script>` beacon. Works on GitHub Pages without moving DNS. Pageviews, referrers, countries, Core Web Vitals. |
| GoatCounter | Free for non-commercial/personal; donation asked for commercial | No cookies, no banner | GoatCounter account | Open source, simple. Public dashboards are possible (nice for showing sponsors). |

**Recommendation: Cloudflare Web Analytics.** It's free for a commercial project like this one (SkillMaxx sells sponsorships), needs no consent banner, and adds one script tag. Brandon needs to create the free Cloudflare account. After that it's a one-line change in `src/_includes/base.njk`:

```html
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "<TOKEN>"}'></script>
```

Not added yet, because there's no account or token. No account was created.
