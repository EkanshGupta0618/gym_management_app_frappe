# Gym Management

Gym Management is a Frappe v15 app for managing members, memberships, lockers, trainers, group classes, and workout plans. The app source is in [apps/gym_management](apps/gym_management).

## Local development setup

Install Frappe Bench and the Frappe v15 prerequisites, including Python 3.10+, Node.js 18+, Yarn, MariaDB, Redis, and Git. Start MariaDB before creating the site. See the [Frappe installation guide](https://docs.frappe.io/framework-git/getting-started/installation).

From this project directory, create a fresh Bench alongside the checkout and copy the app into it. Run the following commands in the same shell.

```bash
project_dir="$(pwd)"
cd ..
bench init --frappe-branch version-15 gym-bench
cd gym-bench

cp -R "$project_dir/apps/gym_management" apps/
bench pip install -e apps/gym_management
printf '%s\n' gym_management >> sites/apps.txt
bench build --app gym_management

bench new-site gym.localhost
bench --site gym.localhost install-app gym_management
bench start
```

When prompted, enter the MariaDB credentials and set the site's Administrator password. Open [Gym Management Desk](http://gym.localhost:8000/app) and sign in as `Administrator`.

If you already have a Bench with Gym Management installed on `gym.localhost`, run `bench start` from that Bench directory. After updating the app code there, apply schema and fixture changes with `bench --site gym.localhost migrate`.

The fresh Bench uses its own copy of the app. Edit the app in that Bench for local testing and copy source changes back to this checkout before committing.
