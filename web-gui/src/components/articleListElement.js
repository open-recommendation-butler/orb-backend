import moment from 'moment';

function ArticleListElement({ article }) {
  return (
    <a href={article.url} key={article.id} target="_blank">
      <div className="my-3 hover:underline">
        <div className="text-sm text-gray-600 flex items-center">
          <div className='shrink text-ellipsis overflow-hidden truncate'>{article.portal} </div>
          <div className='min-w-fit'>&nbsp;|&nbsp;{moment(article.created).fromNow()} </div>
          {article.content_type === 'podcast' &&
            <>
                &nbsp;|&nbsp;
                <svg className="mr-1 min-w-fit" width="9" height="11" viewBox="0 0 320 396" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="103" y="30" width="117" height="200" rx="100" stroke="#475569" strokeWidth="65"/>
                  <path d="M19.013 160C18.3289 212 44.3795 316 154.055 316C263.73 316 301 227.388 301 160" stroke="#475569" strokeWidth="65"/>
                  <path d="M159 314V371" stroke="#475569" strokeWidth="65"/>
                  <path d="M53 377H261" stroke="#475569" strokeWidth="65"/>
                </svg>
                Podcast            
            </>

          }</div>
        <p>{article.title}</p>
        <p className='text-sm mt-2 text-gray-800'>{article.teaser ? article.teaser.slice(0,300) : ' ;'}{article.teaser && article.teaser.length > 300 && '...'}</p>
      </div>
    </a>
  )
}

export default ArticleListElement;