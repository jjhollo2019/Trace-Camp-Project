from django.db import models
from django.urls import reverse_lazy
from service.generator import imageGen

# Create your models here.
class FOAAS(models.Model):
    box_1 = models.TextField(blank=True)
    box_2 = models.TextField(blank=True)
    box_3 = models.TextField(blank=True)
    foaas_message = models.TextField()
    message_url = models.URLField()
    image_url = models.URLField()

    def save(self):
        image = imageGen.ImageGenerator()
        self.image_url = image.generateImage(self.foaas_message)
        super(FOAAS, self).save()

    def get_absolute_url(self):
        return reverse_lazy('FOAAS_detail', args = [str(self.id)])

    def __str__(self):
        return self.foaas_message

class APIEndPoint(models.Model):
    display_name = models.TextField()
    fields = models.TextField()
    url = models.TextField()
    
    def __str__(self):
        return f'{self.display_name}'
    
    def render_url(self, form_input):
        rendered_url = self.url
        for key, value in form_input.items():
            rendered_url = rendered_url.replace(f':{key}', value)
        return rendered_url
    
    def get_fields(self):
        return [field['field'] for field in eval(self.fields)]
