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
- [ ] Unicity constraints in models:
  - [ ] Artist name should be unique
- [ ] Images :
  - [ ] Store as BLOB => https://stackoverflow.com/questions/34598299/store-blob-image-on-server-with-python
  - [ ] Admin : ajouter une photo à un disque
  - [ ] Views : afficher les photos
- [x] Change admin language and TIME_ZONE
- tests : fixtures + tester les associations


ajouter yaml dans requirements
est-ce la bonne manière de faire un formulaire ?

Tests intéressant à faire pour refacto :
- actuellement, un CD ne peut être réservé qu'une fois ! Pourquoi car une réservation n'a qu'un CD et un CD n'a qu'une réservation... Donner la possibilité d'en avoir plusieurs pour éviter une erreur dans `contact`.
