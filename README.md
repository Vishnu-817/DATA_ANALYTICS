# Olive & Ember Restaurant

A responsive restaurant website built with HTML, CSS, JavaScript, Flask, and MySQL.

## Run locally

Requirements: Python 3.12 and MySQL.

1. Create a virtual environment and install packages:

   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Run `schema.sql` in MySQL Workbench or the MySQL CLI.

3. Create your local environment file and enter your own MySQL settings:

   ```powershell
   Copy-Item .env.example .env
   ```

   Set `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` in `.env`.

4. Run the app:

   ```powershell
   python -m flask --app app run --debug
   ```

5. Open <http://127.0.0.1:5000>.

## Deploy from GitHub to Vercel

1. Create an empty repository on GitHub, then run these commands from the project folder (replace the remote URL with your repository URL):

   ```powershell
   git init
   git add .
   git status --short
   git commit -m "Prepare restaurant site for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   git push -u origin main
   ```

   Check that `.env` is not listed by `git status --short`. Do not push passwords or `.venv`.
2. In Vercel, choose **Add New → Project** and import the GitHub repository. Vercel detects the Flask app from `app.py` and installs dependencies from `requirements.txt`.
3. Use a MySQL database reachable from Vercel, such as a managed cloud MySQL service. A MySQL server running on your personal computer (`localhost` or its computer name) is not reachable by a deployed Vercel app.
4. Run `schema.sql` against that cloud database.
5. In **Vercel Project → Settings → Environment Variables**, add `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`. Use the cloud provider's connection details and networking/TLS requirements. Never put production credentials in GitHub or frontend code.
6. Redeploy after setting the environment variables.

The frontend assets are in `public/` for Vercel static delivery. Menu items are read from MySQL; reservations are validated by Flask and inserted into the `reservations` table.

## Checks

Run the test suite with:

```powershell
python -m unittest discover -s tests
```
