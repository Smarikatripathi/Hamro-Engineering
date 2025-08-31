# Code Citations

## License: unknown
https://github.com/piterma98/Tire_workshop_api/tree/8746ee8106e8972a00b12de889f39009dc3c8156/accounts/manager.py

```
'@')[0]
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, *
```


## License: unknown
https://github.com/rayhanhossen/django-experiment/tree/7bab28343a80c573f1d349be688c5ca144009560/user/models.py

```
user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault
```


## License: unknown
https://github.com/umutbrkee/projects/tree/d8a43ddc94475919ec23ee4fbb6f671eb63cfeb0/Software%20Engineering%20Project/FitEats/Main/models.py

```
)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
```

