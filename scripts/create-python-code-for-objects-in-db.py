from django.apps import apps
from django.db import models

def generate_python_code_for_models(*model_names):
    output = ["from django.db import models", "from datetime import date, datetime, time"]
    for model_name in model_names:
        app_label, model_label = model_name.split('.')
        model = apps.get_model(app_label, model_label)
        queryset = model.objects.all()
        for obj in queryset:
            field_assignments = []
            for field in model._meta.get_fields():
                if isinstance(field, (models.ManyToOneRel, models.ManyToManyRel, models.ManyToManyField)):
                    continue
                if field.name == 'contact_person':
                    value_repr = repr('')
                elif isinstance(field, models.ForeignKey):
                    field_name = f"{field.name}_id"
                    value = getattr(obj, field.name + "_id", None)
                    value_repr = str(value) if value is not None else "None"
                else:
                    value = getattr(obj, field.name)
                    if value is None:
                        value_repr = "None"
                    elif isinstance(field, models.DateField):
                        value_repr = f"date({value.year}, {value.month}, {value.day})"
                    elif isinstance(field, models.DateTimeField):
                        value_repr = f"datetime({value.year}, {value.month}, {value.day}, {value.hour}, {value.minute}, {value.second}, {value.microsecond})"
                    elif isinstance(field, models.TimeField):
                        value_repr = f"time({value.hour}, {value.minute}, {value.second}, {value.microsecond})"
                    elif isinstance(value, str):
                        value_repr = repr(value)
                    else:
                        value_repr = str(value)
                field_assignments.append(f"{field_name if isinstance(field, models.ForeignKey) else field.name}={value_repr}")
            assignments_str = ", ".join(field_assignments)
            output.append(f"    {model_label}.objects.create({assignments_str})")
    return "\n".join(output)

model_code = generate_python_code_for_models(
    "locations.District",
    "locations.Location",
    "campaigns.CampaignLocationShift",
)

print(model_code)
