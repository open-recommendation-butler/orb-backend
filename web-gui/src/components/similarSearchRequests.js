function SimilarSearchRequests({similar_search_requests}) {

  if (!similar_search_requests) return;

  return (
    <div className="max-w-xl mt-8">
      <h3 className="text-xl font-bold mb-6">Similar search requests</h3>
      <div className="grid sm:grid-cols-2 gap-3">
        {similar_search_requests.map((simSearch) => 
        <a href={`/search?q=${simSearch}`}>
          <div className="rounded-full bg-slate-200 py-3 px-4 flex items-center hover:underline hover:bg-slate-300">
              <svg className="mr-4 min-w-[20px]" width="20" height="20" viewBox="0 0 477 448" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="184" cy="176" r="157" stroke="#475569" strokeWidth="55"/>
                <path d="M298 269L463.5 434.5" stroke="#475569" strokeWidth="55"/>
              </svg>
              <div className="break-all">{simSearch}</div>
            </div>
          </a>
        )}
      </div>
    </div>
  )
}

export default SimilarSearchRequests;