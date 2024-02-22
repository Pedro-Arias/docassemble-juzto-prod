from docassemble.webapp.users.models import Calendar, DniGroups, DniTypess, DniTypeGroup, Cities
def prueba():
  dnis=[]
  for dni in DniTypess.query.with_entities(DniTypess.code, DniTypess.name, DniTypess.name+" - ("+DniTypess.code+") ").join(DniTypeGroup, DniTypeGroup.typedni == DniTypess.id).join(DniGroups, DniGroups.id == DniTypeGroup.groupdni).filter(DniGroups.code == 'N').all():
    if not dni[1] in dnis:
      dnis.append(dni[1])
  return dnis

