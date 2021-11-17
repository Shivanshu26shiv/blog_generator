# For reference:
# https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
# https://medium.com/the-data-science-publication/how-to-use-the-pytrends-api-to-get-google-trends-data-4378acbaaa8a

need_short_blog = True  # False not recommended since it fetches full wiki content
trends_of_last_these_years = 4
blog_related_to_keyword = ["python"]  # only 1 element

accepted_list = ['JavaScript library', 'Abstract data type', 'Computer science', 'Front-end framework', 'Software',
                 'Type of software', 'Software classification', 'Software developer', 'Computer graphics',
                 'Field of study', 'Computer program', 'Python distribution', 'Graphics',
                 'Programming language', 'Computer programming', 'Package manager', 'Database']


def main():

    from pytrends.request import TrendReq
    pytrends = TrendReq(hl='en-US', tz=360)
    from time import sleep
    sleep(3)
    from datetime import datetime, timedelta
    date_range = \
        (datetime.now() - timedelta(days=trends_of_last_these_years*365)).strftime('%Y-%m-%d') + ' ' + datetime.now().strftime('%Y-%m-%d')
    print('date_range: {}'.format(date_range))
    pytrends.build_payload(kw_list=blog_related_to_keyword, timeframe=date_range, geo='US')
    df_rt = pytrends.related_topics()

    if not df_rt:
        return {}

    search_query = {}

    for topic_cat in ['rising', 'top']:
        if blog_related_to_keyword[0] not in df_rt:
            continue
        topic_raw = df_rt[blog_related_to_keyword[0]][topic_cat].to_dict()
        for topic_index, topic_name in topic_raw['topic_title'].items():
            if topic_raw['topic_type'].get(topic_index, '') in accepted_list:
                # print('topic_name: {}'.format(topic_name), '--', topic_raw['topic_type'].get(topic_index, ''))
                search_query[topic_name.lower()] = topic_raw['topic_type'].get(topic_index, '').lower()

    print('search_query: {}'.format(search_query))

    return search_query


if __name__ == '__main__':

    wiki_summary = ''
    wiki_search_query = main()
    if not wiki_search_query:
        print('No results!')
        exit()

    import random
    random_wiki_query = dict(random.sample(wiki_search_query.items(), 1))

    final_topic_name = list(random_wiki_query.keys())[0]
    final_wiki_query = final_topic_name+' "'+list(random_wiki_query.values())[0] + '"'
    print('\nfinal_wiki_query: {}'.format(final_wiki_query))
    import wikipedia
    if need_short_blog:
        wiki_summary = wikipedia.summary(final_wiki_query, sentences=10)
    else:
        wiki_summary = wikipedia.page(final_wiki_query).content

    import re
    wiki_summary = re.sub('===.*?===', '', wiki_summary)
    wiki_summary = re.sub('==.*?==', '', wiki_summary)
    wiki_summary.replace('\r\n', '')

    if wiki_summary:
        from text_changer import generate_summary
        summarize_text = generate_summary(wiki_summary, top_n=40 if need_short_blog else 10)
        print('\n')
        print('*'*50)
        print('Topic: {} (len: {})'.format(final_topic_name, len(summarize_text)))
        print('\n{}'.format(summarize_text))
        print('*'*50)
        print('\n')
