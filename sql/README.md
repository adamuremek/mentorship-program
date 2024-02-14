# SQL Queries

this folder is for sql queries that are not inteanded to be run directly
by the application, and instead only used in setting the application up

basically think database initilization and the like, we will need a way to get
these to run on install, some kind of install script will be manditory I suspect

anyways yeah sql files for queries here :)

the following command can be used to run these files on unix systems
im not quite sure how to run them on windows though, so if someone
wants to update the README with that info that would be coolio

```bash
psql < <file.sql>
```
> note the above command only works if the account it runs on has permission
> to access the postgresql database, if the command fails try granting
> permisions to the account you are currently on


```

may the sql cat watch over your queries

Art by Joan Stark
      \    /\
       )  ( ')
      (  /  )
jgs    \(__)|
```
