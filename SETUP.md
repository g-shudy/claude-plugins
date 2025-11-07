# Setup Instructions

Complete guide to publishing your g-shudy plugin marketplace.

## ✅ What's Already Done

Your local repository is ready with:
- ✅ Marketplace catalog (`.claude-plugin/marketplace.json`)
- ✅ Example plugin (`hello-world`)
- ✅ GitHub Pages configuration (`CNAME` → `plugins.ghsj.me`)
- ✅ Documentation and licensing
- ✅ Git repository initialized with initial commit

## 📋 Next Steps

### Step 1: Create GitHub Repository

**Option A: Using GitHub CLI (if installed)**
```bash
cd ~/Projects/claude-plugins
gh repo create claude-plugins --public --source=. --remote=origin --push
```

**Option B: Using GitHub Web Interface**

1. Go to https://github.com/new
2. Create new repository:
   - **Name**: `claude-plugins`
   - **Description**: "Personal Claude Code plugin marketplace"
   - **Visibility**: Public
   - **DO NOT** initialize with README/LICENSE/gitignore (we have them)
3. Click "Create repository"

4. Push your local code:
```bash
cd ~/Projects/claude-plugins
git remote add origin git@github.com:g-shudy/claude-plugins.git
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to: https://github.com/g-shudy/claude-plugins/settings/pages
2. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/docs`
3. Click "Save"

4. Wait ~2 minutes, then verify:
   - Site will be live at: `https://g-shudy.github.io/claude-plugins/`

### Step 3: Configure DNS (Your DNS Provider)

Add a CNAME record:

```
Type:  CNAME
Name:  plugins
Value: g-shudy.github.io
TTL:   Auto or 3600
```

**Where to add this:**
- If using Cloudflare: DNS → Records → Add record
- If using Namecheap: Domain List → Manage → Advanced DNS
- If using GoDaddy: DNS → Add → CNAME

**Important:**
- Use `plugins` as the name (not `plugins.ghsj.me`)
- Point to `g-shudy.github.io` (not the full URL with /claude-plugins)

### Step 4: Verify Custom Domain in GitHub

1. Go back to: https://github.com/g-shudy/claude-plugins/settings/pages
2. Under "Custom domain", you should see: `plugins.ghsj.me` ✅
3. Wait for DNS check to complete (~5-10 minutes)
4. Check "Enforce HTTPS" once DNS propagates

### Step 5: Test Your Marketplace

```bash
# Add your marketplace to Claude Code
/plugin marketplace add g-shudy/claude-plugins

# Verify it's added
/plugin marketplace list

# Install the example plugin
/plugin install hello-world@g-shudy-plugins

# Test it
/hello
```

## 🌐 Your Live URLs

Once DNS propagates (10-60 minutes):

- **Marketplace**: https://plugins.ghsj.me/
- **GitHub Repo**: https://github.com/g-shudy/claude-plugins
- **Main Site**: https://ghsj.me (unchanged)

## 🔧 DNS Propagation Check

```bash
# Check if DNS is working
dig plugins.ghsj.me

# Should show:
# plugins.ghsj.me. 3600 IN CNAME g-shudy.github.io.
```

## 📝 What to Tell Your DNS Provider

**If they ask what you're pointing to:**

> I'm setting up a subdomain (plugins.ghsj.me) to point to my GitHub Pages site.
> I need to add a CNAME record:
>
> Name: plugins
> Type: CNAME
> Value: g-shudy.github.io

## 🎉 Success Checklist

- [ ] GitHub repo created and code pushed
- [ ] GitHub Pages enabled (Settings → Pages)
- [ ] DNS CNAME record added
- [ ] Custom domain verified in GitHub
- [ ] HTTPS enforced (after DNS propagates)
- [ ] Website loads at https://plugins.ghsj.me/
- [ ] Marketplace works: `/plugin marketplace add g-shudy/claude-plugins`

## 🚀 Adding More Plugins

```bash
cd ~/Projects/claude-plugins

# Create new plugin structure
mkdir -p plugins/my-new-plugin/{.claude-plugin,commands}

# Add plugin.json, commands, README

# Update marketplace.json to include new plugin

# Commit and push
git add .
git commit -m "feat: add my-new-plugin"
git push

# Install new plugin
/plugin install my-new-plugin@g-shudy-plugins
```

## 🆘 Troubleshooting

### "Site not found" after 10 minutes
- Check DNS propagation: `dig plugins.ghsj.me`
- Verify CNAME record points to `g-shudy.github.io` (not the full URL)

### GitHub Pages shows 404
- Ensure you selected `/docs` folder (not root)
- Check that `docs/index.html` exists in your repo
- Wait a few minutes for GitHub to build

### Custom domain not working in GitHub
- Verify CNAME file contains `plugins.ghsj.me`
- Check DNS has propagated
- Try removing and re-adding the custom domain in Settings → Pages

### Claude Code can't find marketplace
- Ensure repository is public
- Check `.claude-plugin/marketplace.json` exists
- Try the full URL: `/plugin marketplace add https://github.com/g-shudy/claude-plugins`

## 📚 Resources

- **GitHub Pages Docs**: https://docs.github.com/en/pages
- **Claude Code Plugins**: https://docs.claude.com/en/docs/claude-code/plugins
- **Example Marketplace**: https://github.com/jeremylongshore/claude-code-plugins

---

Need help? Check the main [README.md](README.md) or open an issue on GitHub.
