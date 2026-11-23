# Gym Management

A Frappe v15 app to manage a gym: members, memberships, lockers, trainers, classes and workout plans.

## Features
- Member registration and membership plans (auto end date and amount, overlap check)
- Locker booking with double-booking and limit checks
- Trainer subscriptions (amount by duration) and ratings (auto average)
- Group class booking (capacity and duplicate checks), weekly attended-classes email
- Fitness log with Fitness Journey report (member filter and chart)
- Reports: Fitness Journey, Popular Classes, Monthly Revenue
- Workout plans published on the website (`/workout-plans`)
- Member profile page (`/gym_profile`) and custom 404 page
- Roles: Gym Admin, Gym Trainer, Gym Member (exported as fixtures)
- Patch, client scripts and unit tests included

## Installation

See the [project setup guide](../../README.md#local-development-setup).
