from random import choices


def sum_list_items(_list):
    # The nonlocal total binds to this variable.
    total = 0

    def do_the_sum(_list):
        def do_core_computations(_list):
            # Define the total variable as non-local, causing it to bind
            # to the nearest non-global variable also called total.
            nonlocal total
            data = [41, 50, 29]
            random_choices = choices(data, k=len(data))

            for i in _list:
                total += random_choices

        do_core_computations(_list)

    do_the_sum(_list)

    return total


sum_list_items([1, 2, 3])
