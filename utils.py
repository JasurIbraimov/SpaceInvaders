def check_item_clicked(x, y, item):
        return item.left <= x <= item.right  and item.bottom <= y <= item.top