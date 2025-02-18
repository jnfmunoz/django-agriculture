from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Añade una clase CSS personalizada al campo de formulario en Django."""
    return field.as_widget(attrs={'class': css_class})

@register.filter(name='hide_label')
def hide_label(value):
    """
    Este filtro oculta el label en un formulario agregando la clase 'd-none'.
    """
    return value.as_widget(attrs={'class':'d-none'})
