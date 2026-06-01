# Capybara Adventures Website

Static website for capybaraadventures.com — deployable to GitHub Pages in under 5 minutes.

## Files

```
website/
├── index.html      ← Home page
├── books.html      ← All books grid
├── about.html      ← About Capy
├── contact.html    ← Contact form + social links
├── style.css       ← All styles (no framework)
└── assets/
    └── images/     ← Place cover images here (e.g. tokyo-cover.jpg)
```

---

## Deploy to GitHub Pages (Free)

### First time setup

1. Create a new GitHub repository named `capybara-adventures-website`
   (or any name — the repo name doesn't matter if you use a custom domain)

2. Initialize and push this folder:
   ```bash
   cd /Users/jonathan/kdp_coloring_books/website
   git init
   git add .
   git commit -m "Initial website launch"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/capybara-adventures-website.git
   git push -u origin main
   ```

3. In the GitHub repo settings → **Pages** → Source: **Deploy from branch** → Branch: `main` / `/ (root)`

4. Your site will be live at: `https://YOUR_USERNAME.github.io/capybara-adventures-website/`

### Custom domain (capybaraadventures.com)

1. Buy the domain at Namecheap, GoDaddy, or Google Domains (~$12/year)

2. In GitHub Pages settings → Custom domain → enter `capybaraadventures.com`

3. In your domain registrar DNS settings, add these records:
   ```
   A     @    185.199.108.153
   A     @    185.199.109.153
   A     @    185.199.110.153
   A     @    185.199.111.153
   CNAME www  YOUR_USERNAME.github.io
   ```

4. Check "Enforce HTTPS" in GitHub Pages settings (free SSL!)

5. Wait 10-30 minutes for DNS propagation — site is live at capybaraadventures.com ✓

---

## Adding Book Covers

1. Export cover images from `output/kdp_ready/*/` as JPG or PNG
2. Place them in `website/assets/images/` (e.g. `tokyo-cover.jpg`)
3. In `books.html`, replace the emoji `book-cover` divs with:
   ```html
   <div class="book-cover">
     <img src="assets/images/tokyo-cover.jpg" alt="Capybara Adventures: Tokyo" />
   </div>
   ```

---

## Adding Amazon Links

In `books.html` and `index.html`, replace `href="https://amazon.com"` with the actual KDP product page URL after publishing.

---

## Contact Form Setup (Free)

The contact form uses [Formspree](https://formspree.io) — free for 50 submissions/month.

1. Sign up at formspree.io
2. Create a new form → copy your Form ID (looks like `xyzabcde`)
3. In `contact.html`, replace `YOUR_FORM_ID` in the action URL:
   ```html
   action="https://formspree.io/f/xyzabcde"
   ```
4. Remove the `onsubmit="handleSubmit(event)"` attribute (let it submit naturally)
5. Remove the `<script>` block at the bottom of contact.html

---

## Updating the Series List

In `books.html` and `index.html`, update the book cards as new titles are published.
In `index.html`, the featured books section shows 4 titles — keep this to the 4 most recent.

---

## SEO Checklist

- [ ] Update `<meta name="description">` on each page with unique descriptions
- [ ] Replace `href="https://amazon.com"` with real Amazon product URLs
- [ ] Add Google Analytics (paste script before `</head>`)
- [ ] Submit sitemap to Google Search Console after launch
- [ ] Add real cover images (improves click-through from search)
