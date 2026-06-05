# Northwind Robotics — Product & Support FAQ

> Sample knowledge base for the RAG chatbot demo. All products and specs below
> are fictional.

## Product Lineup

Northwind Robotics sells three main products:

1. **Haul-200** — an autonomous mobile robot (AMR) for moving pallets in
   warehouses. Payload capacity is **200 kg**, top speed **2.0 m/s**, and
   battery life **9 hours** per charge.
2. **Haul-500** — a larger AMR with a **500 kg** payload, top speed **1.5 m/s**,
   and **7 hours** of battery life. It supports hot-swappable batteries.
3. **FleetMind** — the cloud software platform that coordinates a fleet of
   robots, plans routes, and integrates with warehouse management systems (WMS).

## Pricing

The Haul-200 starts at **$28,000** per unit. The Haul-500 starts at **$46,000**
per unit. FleetMind is sold as an annual subscription priced at **$3,000 per
robot per year**, which includes software updates and standard support.

Volume discounts begin at 10 units. Educational and research institutions
receive a 15% discount on hardware.

## Warranty and Support

All hardware ships with a **two-year limited warranty** covering manufacturing
defects. An extended warranty adds a third year for 12% of the unit price.

Support tiers:

- **Standard** (included with FleetMind): email support, next-business-day
  response, software updates.
- **Premium** ($8,000/year): 24/7 phone support, 4-hour response target, and a
  dedicated account engineer.

Support can be reached at support@northwind.example or +1-503-555-0142.

## Connectivity and Integration

FleetMind exposes a REST API and webhooks. It has pre-built connectors for SAP
EWM, Manhattan WMS, and Blue Yonder. Robots communicate with FleetMind over
Wi-Fi 6; a wired fallback is available for charging docks.

Data is hosted on AWS in the us-west-2 region by default, with an EU option in
eu-central-1 for customers with data-residency requirements.

## Safety

All Northwind robots include lidar and ultrasonic sensors for obstacle
detection and stop within **0.3 meters** of an unexpected obstacle. They comply
with the ISO 3691-4 standard for driverless industrial trucks. Emergency stop
buttons are located on all four sides of each robot.

## Maintenance

Recommended maintenance is every **2,000 operating hours** or every six months,
whichever comes first. FleetMind automatically schedules maintenance reminders
and tracks each robot's operating hours.
