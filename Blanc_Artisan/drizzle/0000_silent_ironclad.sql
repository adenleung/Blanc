CREATE TABLE `carts` (
	`id` text PRIMARY KEY NOT NULL,
	`data` text NOT NULL,
	`updated_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `catalogue` (
	`id` integer PRIMARY KEY NOT NULL,
	`data` text NOT NULL,
	`approved` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `enquiries` (
	`id` text PRIMARY KEY NOT NULL,
	`data` text NOT NULL,
	`status` text DEFAULT 'new' NOT NULL,
	`created_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `events` (
	`id` text PRIMARY KEY NOT NULL,
	`status` text DEFAULT 'received' NOT NULL,
	`created_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `holds` (
	`id` text PRIMARY KEY NOT NULL,
	`order_id` text NOT NULL,
	`resource` text NOT NULL,
	`qty` integer NOT NULL,
	`status` text DEFAULT 'held' NOT NULL
);
--> statement-breakpoint
CREATE TABLE `inventory` (
	`id` text PRIMARY KEY NOT NULL,
	`available` integer NOT NULL,
	`reserved` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `orders` (
	`id` text PRIMARY KEY NOT NULL,
	`token` text NOT NULL,
	`cart_id` text NOT NULL,
	`fingerprint` text NOT NULL,
	`data` text NOT NULL,
	`amount` integer NOT NULL,
	`payment` text DEFAULT 'pending' NOT NULL,
	`fulfilment` text DEFAULT 'not_started' NOT NULL,
	`session_id` text,
	`payment_intent_id` text,
	`expires_at` integer NOT NULL,
	`created_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `outbox` (
	`id` text PRIMARY KEY NOT NULL,
	`order_id` text NOT NULL,
	`kind` text NOT NULL,
	`status` text DEFAULT 'pending' NOT NULL,
	`created_at` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `paid_effects` (
	`id` text PRIMARY KEY NOT NULL,
	`nonce` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `reservation_guards` (
	`id` text PRIMARY KEY NOT NULL,
	`ok` integer NOT NULL,
	CONSTRAINT "reservation_complete" CHECK("reservation_guards"."ok" = 1)
);
--> statement-breakpoint
CREATE TABLE `settings` (
	`key` text PRIMARY KEY NOT NULL,
	`value` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `slots` (
	`id` text PRIMARY KEY NOT NULL,
	`date` text NOT NULL,
	`label` text NOT NULL,
	`capacity` integer NOT NULL,
	`used` integer DEFAULT 0 NOT NULL
);
