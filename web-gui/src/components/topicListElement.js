import moment from 'moment';
import ArticleListElement from './articleListElement';

function TopicListElement({ topic }) {
  return (
    <div className=''>
      <p className='text-m font-bold'>{ topic.keywords.slice(0, 3).join(", ") }</p>
      <div className=''>
        {topic.articles.map(article => <ArticleListElement article={article} />)}
      </div>
    </div>
  )
}

export default TopicListElement;