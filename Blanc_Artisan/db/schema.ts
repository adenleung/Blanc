import {sql} from 'drizzle-orm';
import { sqliteTable, text, integer, check } from 'drizzle-orm/sqlite-core';
export const settings=sqliteTable('settings',{key:text('key').primaryKey(),value:text('value').notNull()});
export const catalogue=sqliteTable('catalogue',{id:integer('id').primaryKey(),data:text('data').notNull(),approved:integer('approved').notNull().default(0)});
export const carts=sqliteTable('carts',{id:text('id').primaryKey(),data:text('data').notNull(),updatedAt:integer('updated_at').notNull(),revision:text('revision').notNull()});
export const orders=sqliteTable('orders',{id:text('id').primaryKey(),token:text('token').notNull(),cartId:text('cart_id').notNull(),fingerprint:text('fingerprint').notNull(),data:text('data').notNull(),amount:integer('amount').notNull(),payment:text('payment').notNull().default('pending'),fulfilment:text('fulfilment').notNull().default('not_started'),sessionId:text('session_id'),paymentIntentId:text('payment_intent_id'),expiresAt:integer('expires_at').notNull(),createdAt:integer('created_at').notNull()});
export const slots=sqliteTable('slots',{id:text('id').primaryKey(),date:text('date').notNull(),label:text('label').notNull(),capacity:integer('capacity').notNull(),used:integer('used').notNull().default(0)});
export const inventory=sqliteTable('inventory',{id:text('id').primaryKey(),available:integer('available').notNull(),reserved:integer('reserved').notNull().default(0)});
export const holds=sqliteTable('holds',{id:text('id').primaryKey(),orderId:text('order_id').notNull(),resource:text('resource').notNull(),qty:integer('qty').notNull(),status:text('status').notNull().default('held')});
export const events=sqliteTable('events',{id:text('id').primaryKey(),status:text('status').notNull().default('received'),createdAt:integer('created_at').notNull()});
export const enquiries=sqliteTable('enquiries',{id:text('id').primaryKey(),data:text('data').notNull(),status:text('status').notNull().default('new'),createdAt:integer('created_at').notNull()});
export const outbox=sqliteTable('outbox',{id:text('id').primaryKey(),orderId:text('order_id').notNull(),kind:text('kind').notNull(),status:text('status').notNull().default('pending'),createdAt:integer('created_at').notNull()});

export const reservationGuards=sqliteTable('reservation_guards',{id:text('id').primaryKey(),ok:integer('ok').notNull()},t=>[check('reservation_complete',sql`${t.ok} = 1`)]);

export const paidEffects=sqliteTable('paid_effects',{id:text('id').primaryKey(),nonce:text('nonce').notNull()});
