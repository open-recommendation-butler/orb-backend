import moment from 'moment';
import ArticleListElement from './articleListElement';

function TopicListElement({ topic }) {
  return (
    <div className='mb-4'>
      <p className='text-m font-bold'>{ topic.keywords.slice(0, 3).join(", ") }</p>
      <div className='grid md:grid-cols-2 gap-x-3'>
        {topic.articles.map(article => <ArticleListElement article={article} />)}
      </div>
    </div>
  )
}

export default TopicListElement;