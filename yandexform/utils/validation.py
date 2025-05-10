def validate_form_fields(fields):
    if not isinstance(fields, list):
        raise ValueError('Fields must be a list')

    for field in fields:
        if 'type' not in field or 'label' not in field:
            raise ValueError('Each field must have "type" and "label"')

        field_type = field['type']
        if field_type not in ['text', 'radio', 'checkbox']:
            raise ValueError(f'Invalid field type: {field_type}')

        if field_type in ['radio', 'checkbox']:
            if 'options' not in field or not isinstance(field['options'], list):
                raise ValueError(f'Options are required for {field_type} field')
            if len(field['options']) < 2:
                raise ValueError(f'At least 2 options required for {field_type} field')


def validate_response(form_fields, answers):
    for field in form_fields:
        label = field['label']
        if label not in answers:
            raise ValueError(f'Ответ на поле "{label}" отсутствует')

        field_type = field['type']
        answer = answers[label]

        if field_type == 'text' and not isinstance(answer, str):
            raise ValueError(f'Поле "{label}" должно быть текстом')

        if field_type in ['radio', 'checkbox']:
            valid_options = field['options']
            if isinstance(answer, list):
                for a in answer:
                    if a not in valid_options:
                        raise ValueError(f'Недопустимый вариант в поле "{label}"')
            else:
                if answer not in valid_options:
                    raise ValueError(f'Недопустимый вариант в поле "{label}"')