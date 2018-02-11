from pynamodb.models import Model
from pynamodb.attributes import ListAttribute, UTCDateTimeAttribute, NumberAttribute, \
    MapAttribute, UnicodeAttribute, UnicodeSetAttribute
from pynamodb.indexes import LocalSecondaryIndex, AllProjection

class Project(Model):
    class Meta:
        table_name = 'projects'
        region = 'eu-west-1'
    
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    members = UnicodeSetAttribute(null=True)
    owner = UnicodeAttribute()

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'owner', self.owner
        yield 'members', list(self.members) if self.members is not None else []

    def all_members(self):
        return (self.members if self.members is not None else set()) | {self.owner}

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
    points = NumberAttribute(null=True)

    def output_dict(self, sprint):
        yield 'id', self.id
        yield 'sprint_id', sprint.id
        yield 'project_id', sprint.project_id
        yield 'name', self.name
        yield 'description', self.description if self.description is not None else ''
        yield 'points', self.points

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

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name
        yield 'project_id', self.project_id
        yield 'start_date', self.start_date.strftime('%Y-%m-%d')
        yield 'end_date', self.end_date.strftime('%Y-%m-%d')
        yield 'swimlanes', [dict(x.output_dict(self)) for x in self.swimlanes] if self.swimlanes is not None else []

class TaskSprintIndex(LocalSecondaryIndex):
    class Meta:
        index_name = 'project_id-sprint_id-index'
        projection = AllProjection()

    project_id = UnicodeAttribute(hash_key=True)
    sprint_id = UnicodeAttribute(range_key=True)

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
    sprint_index = TaskSprintIndex()

    def __iter__(self):
        yield 'id', self.id
        yield 'project_id', self.project_id
        yield 'sprint_id', self.sprint_id
        yield 'swimlane_id', self.swimlane_id
        yield 'state', self.state
        yield 'name', self.name
        yield 'description', self.description
        yield 'planned_points', self.planned_points
        yield 'points', self.points
        yield 'assigned_members', list(self.assigned_members) if self.assigned_members is not None else []
