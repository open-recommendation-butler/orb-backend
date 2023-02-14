import moment from 'moment';
import ArticleListElement from './articleListElement';

function TopicListElement({ topic }) {
  return (
    topic.article_count === 1
      ? <ArticleListElement article={topic.articles[0]} />
      :
        <div className='mb-4 border-t border-b pt-2'>
          <p className='text-m font-bold'>{ topic.keywords.slice(0, 3).join(", ") }</p>
          <div className='grid md:grid-cols-2 gap-x-3'>
            {topic.articles.map(article => <ArticleListElement article={article} />)}
          </div>
        </div>
  )
}

export default TopicListElement;