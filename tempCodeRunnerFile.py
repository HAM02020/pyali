if __name__ == "__main__":

    url = 'https://www.aliexpress.com/all-wholesale-products.html'
    html = gethtml_withcache(url)
    categories = parseCategories()
    export_csv(categories)