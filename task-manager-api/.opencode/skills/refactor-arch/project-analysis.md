# Project Analysis Heuristics

Use these heuristics to detect the technology stack, framework, database, and domain of any project.

---

## Language Detection

| Signal | Language |
|--------|----------|
| `requirements.txt`, `setup.py`, `pyproject.toml`, `.py` files | Python |
| `package.json`, `.js` / `.ts` files | JavaScript / TypeScript |
| `go.mod`, `.go` files | Go |
| `Gemfile`, `.rb` files | Ruby |
| `pom.xml`, `build.gradle`, `.java` files | Java |
| `Cargo.toml`, `.rs` files | Rust |
| `composer.json`, `.php` files | PHP |
| `.csproj`, `.sln`, `.cs` files | C# |

### Python Version Detection
- Check `python_requires` in `setup.py` or `pyproject.toml`
- Check `python` field in `pyproject.toml`
- Check `.python-version` file
- Check shebang lines (`#!/usr/bin/env python3`)

### Node.js Version Detection
- Check `engines.node` in `package.json`
- Check `.nvmrc` or `.node-version` file

---

## Framework Detection

### Python Frameworks

| Signal | Framework |
|--------|-----------|
| `from flask import Flask` or `flask` in requirements.txt | Flask |
| `from fastapi import FastAPI` or `fastapi` in requirements.txt | FastAPI |
| `import django` or `django` in requirements.txt | Django |
| `from sanic import Sanic` or `sanic` in requirements.txt | Sanic |
| `from bottle import` or `bottle` in requirements.txt | Bottle |
| `import tornado` or `tornado` in requirements.txt | Tornado |

### Node.js Frameworks

| Signal | Framework |
|--------|-----------|
| `require('express')` or `express` in package.json | Express |
| `require('koa')` or `koa` in package.json | Koa |
| `require('fastify')` or `fastify` in package.json | Fastify |
| `require('hapi')` or `@hapi/hapi` in package.json | Hapi |
| `nest` or `@nestjs` in package.json | NestJS |

### Framework Version Detection
- Read `requirements.txt` for exact version pins (e.g., `flask==3.1.1`)
- Read `package.json` for version ranges (e.g., `"express": "^4.18.2"`)
- Check `package-lock.json` for resolved versions

---

## Database Detection

### Drivers and ORMs

| Signal | Database | Type |
|--------|----------|------|
| `import sqlite3` or `sqlite3` in package.json | SQLite | Driver |
| `import psycopg2` or `psycopg2` in requirements | PostgreSQL | Driver |
| `import pymysql` or `pymysql` in requirements | MySQL | Driver |
| `from sqlalchemy import` or `sqlalchemy` in requirements | SQLAlchemy (Python ORM) | ORM |
| `flask_sqlalchemy` in requirements | Flask-SQLAlchemy | ORM |
| `require('mongoose')` or `mongoose` in package.json | Mongoose (MongoDB ODM) | ODM |
| `require('sequelize')` or `sequelize` in package.json | Sequelize (SQL ORM) | ORM |
| `require('typeorm')` or `typeorm` in package.json | TypeORM | ORM |
| `require('knex')` or `knex` in package.json | Knex.js (query builder) | Query Builder |
| `require('prisma')` or `prisma` in package.json | Prisma | ORM |
| `from google.cloud import firestore` | Firestore | Cloud DB |

### Connection Detection
- Look for connection strings: `sqlite:///`, `postgresql://`, `mysql://`, `mongodb://`, `mysql+pymysql://`
- Look for `sqlite3.connect()` calls
- Look for `create_engine()` calls (SQLAlchemy)
- Look for `new sqlite3.Database()` calls (Node.js)

### Table/Model Detection
- Read `CREATE TABLE` SQL statements
- Read SQLAlchemy model classes (`class TableName(db.Model)`)
- Read Mongoose schema definitions (`new Schema({...})`)
- Read Sequelize model definitions (`sequelize.define(...)`)

---

## Domain Detection

Analyze route/endpoint names and model/table names to infer the application domain.

### Route Pattern Analysis

| Route Pattern | Likely Domain |
|---------------|---------------|
| `/products`, `/items`, `/catalog` | E-commerce / Product catalog |
| `/users`, `/accounts`, `/auth` | User management |
| `/orders`, `/cart`, `/checkout` | E-commerce / Order management |
| `/courses`, `/lessons`, `/enrollments` | Education / LMS |
| `/tasks`, `/todos`, `/projects` | Task management / Project management |
| `/posts`, `/comments`, `/feeds` | Content management / Social |
| `/patients`, `/appointments`, `/records` | Healthcare |
| `/invoices`, `/payments`, `/billing` | Finance / Billing |
| `/posts`, `/articles`, `/tags` | Blog / CMS |

### Model/Table Name Analysis

| Model/Table Name | Likely Domain Entity |
|------------------|---------------------|
| `products`, `items` | Products |
| `users`, `accounts`, `members` | Users |
| `orders`, `purchases`, `carts` | Orders |
| `courses`, `lessons`, `modules` | Education content |
| `tasks`, `todos`, `issues` | Tasks |
| `payments`, `transactions` | Payments |
| `categories`, `tags` | Classification |

### Domain Description Format
Combine findings into a 1-sentence description:
> "E-commerce API for managing products, users, and orders"
> "LMS API with course enrollment and checkout flow"
> "Task manager API with users, tasks, categories, and reporting"

---

## Architecture Pattern Detection

### Current Architecture Classification

| Pattern | Signals |
|---------|---------|
| **Flat / Monolithic** | All code in root-level files, no subdirectories for logic |
| **Partially Organized** | Some directories (models/, routes/) but missing layers (no controllers/, services/) |
| **MVC** | Separate models/, views/ (or routes/), controllers/ directories |
| **Layered** | Separate models/, services/, repositories/, controllers/ directories |
| **Clean Architecture** | domain/, application/, infrastructure/, presentation/ directories |

### File Count Analysis
- Count total source files (excluding config, tests, migrations)
- Count lines of code per file
- Identify the largest file(s) — potential God files
- Identify files with mixed responsibilities

---

## Entry Point Detection

| Language | Common Entry Points |
|----------|-------------------|
| Python/Flask | `app.py`, `wsgi.py`, `manage.py`, `run.py` |
| Python/FastAPI | `main.py`, `app.py` |
| Python/Django | `manage.py`, `wsgi.py`, `asgi.py` |
| Node.js/Express | `app.js`, `server.js`, `index.js`, `src/app.js`, `src/index.js` |
| Node.js/NestJS | `src/main.ts` |
| Go | `main.go`, `cmd/*/main.go` |
| Ruby/Rails | `config.ru`, `bin/rails` |

---

## Dependency Analysis

### Python
- Read `requirements.txt` for direct dependencies
- Distinguish between:
  - **Web framework** (flask, fastapi, django)
  - **Database** (sqlalchemy, psycopg2, pymongo)
  - **Utilities** (python-dotenv, requests, marshmallow)
  - **Testing** (pytest, unittest)
  - **Linting** (flake8, black, pylint)

### Node.js
- Read `package.json` for `dependencies` and `devDependencies`
- Distinguish between:
  - **Web framework** (express, fastify, koa)
  - **Database** (mongoose, sequelize, pg, sqlite3)
  - **Utilities** (lodash, moment, dotenv)
  - **Testing** (jest, mocha, chai)
  - **Build tools** (webpack, babel, typescript)

---

## Technology-Agnostic Checklist

When analyzing any project, answer these questions:

1. What programming language is this?
2. What web framework is used?
3. What database/ORM is used?
4. What is the application domain?
5. What is the current architecture pattern?
6. Where is the entry point?
7. How many source files are there?
8. What is the largest file? (potential God file)
9. Are there separate layers for models, routes, controllers?
10. Are there any configuration files with hardcoded values?
