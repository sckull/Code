
## Virtualenv & dependencies
```
virtualenv friend
source friend/bin/activate
pip install -r req.txt
```

## Create db
```
python
>> from app import db
>> db.create_all()
>> exit()
```

**If error creating db.**
```
pip install 'SQLAlchemy<1.4.0'
```
