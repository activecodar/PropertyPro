from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
from rest_framework import status


def get_model_object(model, column_name, column_value, **kwargs):
    """
    Gets model instance from the database by a certain field.
    Args:
        model: Holds the model from which we want to query data
        column_name: Holds the model field to query data by from the model.
        column_value: Holds the value for the column_name.
        kwargs : Hold optional keyword arguments.
    Returns:
        model_instance: If the value exists or not, at checks of
         column_name id having column_value as an int and
         greater or equal to one, or column_name id having
         column_value as a string, or any other column_name being
         any name other than id.
        error: Else exception is raised with appropriate message.
    """
    manager_query = kwargs.get('manager_query', model.objects)
    try:
        if ((column_name == "id") and isinstance(column_value, int) and
                (column_value < 1)):
            error_message = f"id does not exist from column {column_value}"
            APIException.status_code = status.HTTP_404_NOT_FOUND
            raise APIException({"error": error_message})
        model_instance = manager_query.get(**{column_name: column_value})
        return model_instance
    except ObjectDoesNotExist:
        APIException.status_code = status.HTTP_404_NOT_FOUND
        raise APIException({"error": f"{column_name} {column_value} was not found in the {model.__name__}'s table."})


def get_query_set(model, **kwargs):
    manager_query = kwargs.get('manager_query', model.objects)
    order_by = kwargs.get('order_by', 'created_at')
    try:
        query_list = manager_query.all().order_by(order_by)
        return query_list
    except ObjectDoesNotExist:
        APIException.status_code = status.HTTP_404_NOT_FOUND
        raise APIException({"error": f"{model} does not exist in the system."})