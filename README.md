[![Build Status](https://travis-ci.org/rohan-panchal/StickShift.svg?branch=master)](https://travis-ci.org/rohan-panchal/StickShift)
[![codecov.io](https://codecov.io/github/rohan-panchal/StickShift/coverage.svg?branch=master)](https://codecov.io/github/rohan-panchal/StickShift)

# StickShift
A Database Migration tool using SQL files as change scripts.

# Supports

| Python |
|:------:|
|   2.7  |
|   3.2  |
|   3.3  |
|   3.4  |
|   3.5  |

| Database Engines |
|:----------------:|
|    PostgreSQL    |

# Installation

`pip install stickshift`

# Setup

Before you create migration scripts you need to setup a migration repository. 
The migration repository is a folder which will hold your upgrade and downgrade sql scripts, 
as well as your configuration file for your database environments. 

To setup the migration repository execute the command:

`stickshift setup`

This will result in the folder structure:

```
+-- db
|   +-- upgrade // This will hold the migration scripts
|   +-- downgrade // This will hold the scripts to tear down changes.
|   +-- database.ini // This will hold configuration data for the specific database.
```

# Configuration

In the migration repository there is a file called `database.ini`. This is for managing database data and environments. 

By default this file contains:

```
[DATABASE]
host: DB_HOST
port: DB_PORT
username: DB_USERNAME
password: DB_PASSWORD
database: DB_NAME
```

The fields `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME` should be replaced either with the appropriate values, or keys corresponding to environment variables. If using specific values, blank values can be used in cases such as password. To use environment variables surround the key with `[]`

Values:

```
[DEVELOPMENT]
host: localhost
port: 5432
username: root
password: 
database: stickshift
```

Environment Variables

```
[PRODUCTION]
host: [DB_HOST]
port: [DB_PORT]
username: [DB_USERNAME]
password: [DB_PASSWORD]
database: [DB_NAME]
```

# Provisioning The Database

Now that you have a migration repository you can provision the database so that it can track migration versions.

To provision the database execute the command:

`stickshift db provision <ENVIRONMENT>`

Where <ENVIRONMENT> is the name of the database environment you'd like to migrate.

Example:

`stickshift db provision DEVELOPMENT`

# Creating Migration Scripts

While all migration scripts are SQL files, the names follow syntax determined by what command you execute, as well as default templates.


## New Table Migrations
To create a new table migration you execute the command:

`stickshift new table <tablename>`

Where 

*  `<tablename>` is the name of the table you would like to create.

Example:

`stickshift new table users`

This will create two migration scripts in the migration repository.

```
+-- db
|   +-- upgrade
|      +-- V00__create_table_users.sql
|   +-- downgrade
|      +-- V00__drop_table_users.sql
|   +-- database.ini
```

As you can see there is an upgrade and a downgrade script. 

The upgrade script results in an empty `CREATE TABLE` statement:

```
/* V00__create_table_users.sql */
CREATE TABLE IF NOT EXISTS users ();
```

The downgrade script results in a `DROP TABLE` statement:

```
/* V00__drop_table_users.sql */
DROP TABLE IF EXISTS users CASCADE;
```

*Note:* If any other statements were added to the upgrade script the opposite must be implemented within the downgrade script.

## Alter Table Migrations
To create a table altering migration you execute the command:

`stickshift alter table <tablename> <change_description>`

Where:

*  `<tablename>` is the name of the table you would like to create.  
*	`<change_description>` is a short description of what changes you are making.


Example:

`stickshift alter users add_id`

This will create two migration scripts in the migration repository.

```
+-- db
|   +-- upgrade
|      +-- V00__create_table_users.sql
|      +-- V01__alter_table_users_add_id.sql
|   +-- downgrade
|      +-- V00__drop_table_users.sql
|      +-- V01__undo_alter_table_users_add_id.sql
|   +-- database.ini
```

*Note:* These migration scripts are blank and require appropriate statements to be filled in.

## New Procedure Migrations
To create a procedure migration you execute the command:

`stickshift new procedure <procedure_name>`

Where:

*	`<procedure_name>` is the name of the procedure you would like to create.

Example:

`stickshift new procedure insert_user`

This will create two migration scripts in the migration repository.

```
+-- db
|   +-- upgrade
|      +-- V00__create_table_users.sql
|      +-- V01__alter_table_users_add_id.sql
|      +-- V02__create_sp_insert_user.sql
|   +-- downgrade
|      +-- V00__drop_table_users.sql
|      +-- V01__undo_alter_table_users_add_id.sql
|      +-- V02__drop_sp_insert_user.sql
|   +-- database.ini
```

The upgrade script results in an empty `CREATE OR REPLACE FUNCTION` statement:

```
/* V02__create_sp_insert_user.sql */
CREATE OR REPLACE FUNCTION sp_insert_user 
(

) 

RETURNS RETURN_TYPE 
(
) AS $$ 

BEGIN 

END; $$ LANGUAGE plpgsql;
```

The downgrade script results in a `DROP FUNCTION IF EXISTS` statement:

```
/* V02__drop_sp_insert_user.sql */
DROP FUNCION IF EXISTS sp_insert_user;
```

# Executing Migration Scripts
## Migrating
To migrate the database to the most current version you execute the command:

`stickshift db migrate <environment>`

Where:

*  `<environment>` is the name of the environment you'd like to migrate.

*Prerequisite:* The migration repository must be setup, and the database must be provisioned.

## Downgrading
To undo all database migrations you execute the command:

`stickshift db downgrade <environment>`

Where:

*  `<environment>` is the name of the environment you'd like to downgrade.

# Fetch Information
## Version
To fetch the current version of a specific database environment execute the command:

`stickshift db version <environment>`

Where:

*  `<environment>` is the name of the environment you'd like to fetch the current version from.

## Tables
To list the current tables in the specific database environment execute the command:

`stickshift db tables <environment>`

Where:

*  `<environment>` is the name of the environment you'd like to fetch the current version from.

## Procedures
To list the current stored procedures in the specific database environment execute the command:

`stickshift db procedures <environment>`

Where:

*  `<environment>` is the name of the environment you'd like to fetch the current version from.


# Command Graph

```
+-- stickshift
|   +-- --help
|
|   +-- setup
|   +-- clear
|   +-- new
|      +-- table
|         +-- <name>
|      +-- procedure
|         +-- <name>
|   +-- alter
|      +-- <tablename>
|         +-- <tablechange>
|   +-- db
|      +-- provision
|      +-- deprovision
|      +-- version
|      +-- versions
|      +-- procedures
|      +-- tables
|      +-- upgrade
|      +-- downgrade
|      +-- reset
+
```