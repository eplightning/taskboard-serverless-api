from pynamodb.models import Model
from pynamodb.attributes import ListAttribute, UTCDateTimeAttribute, NumberAttribute, \
    MapAttribute, UnicodeAttribute, UnicodeSetAttribute

class Project(Model):
    class Meta:
        table_name = 'projects'
        region = 'eu-west-1'
    
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    members = UnicodeSetAttribute(null=True)
    owner = UnicodeAttribute()

class User(Model):
    class Meta:
        table_name = 'users'
        region = 'eu-west-1'

    email = UnicodeAttribute(hash_key=True)
    projects = UnicodeSetAttribute(null=True)

class Swimlane(MapAttribute):
    id = UnicodeAttribute()
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    points = NumberAttribute()

class Sprint(Model):
    class Meta:
        table_name = 'sprints'
        region = 'eu-west-1'

    project_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    start_date = UTCDateTimeAttribute()
    end_date = UTCDateTimeAttribute()
    name = UnicodeAttribute()
    swimlanes = ListAttribute(of=Swimlane, null=True)

class Task(Model):
    class Meta:
        table_name = 'tasks'
        region = 'eu-west-1'
    
    project_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    sprint_id = UnicodeAttribute()
    swimlane_id = UnicodeAttribute(null=True)
    state = UnicodeAttribute()
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    planned_points = NumberAttribute(null=True)
    points = NumberAttribute(null=True)
    assigned_members = UnicodeSetAttribute(null=True)
