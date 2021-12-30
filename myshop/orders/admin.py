import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe


class OrderItemInline(admin.TabularInline):
    '''Class to include the OrderItem on the same page as the OrderAdmin page.'''
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    '''Custom admin action to download a list of orders as a CSV file.

    The function performs the following:
    1. Creates an instance of HttpResponse, specifying the text/csv content type,
        to tell the browser the reponse has to be treated as a CSV file. Also adds
        a Content-Disposition header to indicate that the HTTP response contains
        an attached file.
    2. Creates a CSV writer object that will write to the response object.
    3. Get the model fields dynamically using the get_fields() method of the model
        _meta options. Excludes many-to-many and one-to-many relationships.
    4. Writes a header row including the field names.
    5. Iterate over the given QuerySet and write a row for each object returned by
        the QuerySet.
    6. Cutomize the display name for the action in the actions dropdown element of
        the admin site by setting a short_description attribute on the function.

    Args:
        modelAdmin: the current ModelAdmin being displayed. 
        request: The current request object as an HTTPRequest instance.
        queryset: A queryset for the objects selected by the user.

    Returns:
        A generic administration action that can be added to any ModelAdmin class.
    '''
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
#Specifying the name of the dropdown function as 'Export to CSV'
export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    '''Function that takes an Order object as an argument and returns an HTML link for the admin_order_detail URL.'''
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def order_pdf(obj):
    '''Function that takes an Order object as an argument and returns a link to the PDF file for each result.'''
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
#Specifying the name of the columns as 'Invoice'
order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]