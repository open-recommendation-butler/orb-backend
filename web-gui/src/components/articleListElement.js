import moment from 'moment';

function ArticleListElement({ article }) {
  return (
    <a href={article.url} key={article.id} target="_blank">
      <div className="my-3 hover:underline">
        <p className="text-sm text-gray-600">{article.portal} | {moment(article.created).fromNow()}</p>
        <p>{article.title}</p>
        <p className='text-sm mt-2 text-gray-800'>{article.teaser}</p>
      </div>
    </a>
  )
}

export default ArticleListElement;