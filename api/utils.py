

def prev_next_post(obj):
    try:
        prevObj = obj.get_previous_by_created_at()
        prevDict = {
            'id': prevObj.id,
            'title': prevObj.title,
        }
    except obj.DoesNotExist:
        prevDict = {}

    try:
        nextObj = obj.get_next_by_created_at()
        nextDict = {
            'id': nextObj.id,
            'title': nextObj.title,
        }
    except obj.DoesNotExist:
        nextDict = {}

    return prevDict, nextDict


def obj_to_comment(obj):
    """ comment 객체를 serialize 한다. """
    comment = dict(vars(obj))

    if obj.update_dt:
        comment['update_dt'] = obj.update_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        comment['update_dt'] = '9999-12-31 00:00:00'

    del comment['_state'], comment['post_id'], comment['create_dt']

    return comment
