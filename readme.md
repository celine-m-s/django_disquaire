- [x] setup Django project
- [x] models:
  - [x] Artist
  - [x] Disk
  - [x] Booking
  - [x] Contact
- [x] associations : problem with many to many => <class 'manager.admin.DiskInline'>: (admin.E202) 'manager.Disk' has no ForeignKey to 'manager.Artist'.
- [x] Admin
- [x] Use a Postgresql DB
- [x] Views:
  - [x] static files
  - [x] index
  - [x] list albums + paginate (méthode paginate)
  - [x] read
  - [x] search
  - [x] result list
  - [x] contact form
- [x] Transactions
- [x] Unicity constraints in models:
  - [x] Artist name should be unique
- [x] Images :
  - [x] Admin : ajouter une photo à un disque
  - [x] Views : afficher les photos
- [x] Change admin language and TIME_ZONE
- [ ] tests : fixtures + tester les associations


Howto create a user and associated db in postgresql:
sudo -u postgres createuser -D -A -P username
sudo -u postgres createdb -O username dbname
Don't forget to alter the configuration files /etc/postgresql/8.4/main/postgresql.conf (for accessing from localhost) and /etc/postgresql/8.4/main/pg_hba.conf (replacing ident by md5 for all users, so that new user can access db)
