# Somewhat Reunion

A Hugo-based website for the Somewhat Reunion event, built with the [Congo theme](https://github.com/jpanther/congo).

## Prerequisites

- [Hugo](https://gohugo.io/installation/) (Extended version recommended)
- Git (for version control and theme management)

## Local Development

1. Clone the repository and navigate to the project directory:
```bash
git clone <your-repo-url>
cd somewhat
```

2. Install/update the theme:
```bash
git submodule update --init --recursive
```

3. Start the Hugo development server:
```bash
hugo server
```

4. Visit `http://localhost:1313` in your browser

## Building for Production

Generate the static site files:

```bash
hugo --minify
```

This creates a `public/` directory containing all the static files ready for deployment.

## Deployment Instructions

### Option 1: Traditional Web Server (Apache/Nginx)

#### Apache

1. Build the site:
```bash
hugo --minify
```

2. Copy the `public/` directory contents to your web server:
```bash
rsync -avz --delete public/ user@your-server:/var/www/html/
```

3. Configure Apache virtual host (`/etc/apache2/sites-available/somewhat.conf`):
```apache
<VirtualHost *:80>
    ServerName sta.tommertron.com
    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/somewhat_error.log
    CustomLog ${APACHE_LOG_DIR}/somewhat_access.log combined
</VirtualHost>
```

4. Enable the site and restart Apache:
```bash
sudo a2ensite somewhat
sudo systemctl restart apache2
```

#### Nginx

1. Build the site:
```bash
hugo --minify
```

2. Copy files to server:
```bash
rsync -avz --delete public/ user@your-server:/var/www/somewhat/
```

3. Configure Nginx (`/etc/nginx/sites-available/somewhat`):
```nginx
server {
    listen 80;
    server_name sta.tommertron.com;

    root /var/www/somewhat;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # Enable gzip compression
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

4. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/somewhat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Automated Deployment with GitHub Pages

1. Create `.github/workflows/hugo.yml`:
```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true
      - name: Build
        run: hugo --minify
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

### Option 3: Netlify

1. Build command: `hugo --minify`
2. Publish directory: `public`
3. Add `netlify.toml` in project root:
```toml
[build]
  publish = "public"
  command = "hugo --minify"

[build.environment]
  HUGO_VERSION = "0.120.0"
  HUGO_ENV = "production"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
```

### Option 4: Vercel

1. Import your Git repository
2. Set build command: `hugo --minify`
3. Set output directory: `public`
4. Vercel will auto-detect Hugo and deploy

### Option 5: AWS S3 + CloudFront

1. Build the site:
```bash
hugo --minify
```

2. Create an S3 bucket and enable static website hosting

3. Upload files:
```bash
aws s3 sync public/ s3://your-bucket-name/ --delete
```

4. Set up CloudFront distribution pointing to the S3 bucket

## SSL/HTTPS Setup

For Apache/Nginx deployments, use [Let's Encrypt](https://letsencrypt.org/) with Certbot:

```bash
sudo certbot --apache -d sta.tommertron.com  # For Apache
sudo certbot --nginx -d sta.tommertron.com   # For Nginx
```

## Configuration

The main configuration file is `hugo.toml`. Update the following as needed:

- `baseURL`: Your site's URL
- `title`: Site title
- `theme`: Current theme (congo)

## Project Structure

```
.
├── archetypes/      # Content templates
├── assets/          # CSS, JS, images (processed by Hugo)
├── config/          # Configuration files
├── content/         # Markdown content files
├── layouts/         # HTML templates
├── public/          # Generated static site (git ignored)
├── static/          # Static files (copied as-is)
└── themes/          # Hugo themes
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
