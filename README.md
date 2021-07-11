# Question Bank API

You will never confused how to pick the exam quizes and generate PDFs.

## Requirements/Environments

This app is developed with Python3.9.5.
You can install required packages via pip.

You must install `Python3` and `postgresql` with `libpq` packages to your system.

## Development

This is personal developing app, but your pull requesting is really welcomed.

Please folk [mizphses/pyqmake](https://github.com/mizphses.pyqmake) and make a pull request.

## メモ

```sql
CREATE TABLE users (id serial PRIMARY KEY, username varchar UNIQUE, useremail varchar UNIQUE, password_digest varchar, namae varchar);
```
