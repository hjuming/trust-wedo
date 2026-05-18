const pageTitle = '台灣實體書店查詢地圖｜Trust WEDO × Book WEDO'
const pageDescription = '查詢全台大型連鎖書店、獨立書店、7-11 書香門市、經銷書店與圖書館，支援地區、品牌、分類與 Google Maps 導航。'
const coverPath = '/bookstores/cover-bookstore.png'

function absoluteUrl(request, path) {
  const url = new URL(request.url)
  return `${url.origin}${path}`
}

function metaRewriter(request) {
  const pageUrl = new URL('/bookstores', request.url).toString()
  const imageUrl = absoluteUrl(request, coverPath)

  return new HTMLRewriter()
    .on('title', {
      element(element) {
        element.setInnerContent(pageTitle)
      },
    })
    .on('meta[name="title"]', {
      element(element) {
        element.setAttribute('content', pageTitle)
      },
    })
    .on('meta[name="description"]', {
      element(element) {
        element.setAttribute('content', pageDescription)
      },
    })
    .on('meta[property="og:url"]', {
      element(element) {
        element.setAttribute('content', pageUrl)
      },
    })
    .on('meta[property="og:title"]', {
      element(element) {
        element.setAttribute('content', pageTitle)
      },
    })
    .on('meta[property="og:description"]', {
      element(element) {
        element.setAttribute('content', pageDescription)
      },
    })
    .on('meta[property="og:image"]', {
      element(element) {
        element.setAttribute('content', imageUrl)
      },
    })
    .on('meta[property="twitter:url"]', {
      element(element) {
        element.setAttribute('content', pageUrl)
      },
    })
    .on('meta[property="twitter:title"]', {
      element(element) {
        element.setAttribute('content', pageTitle)
      },
    })
    .on('meta[property="twitter:description"]', {
      element(element) {
        element.setAttribute('content', pageDescription)
      },
    })
    .on('meta[property="twitter:image"]', {
      element(element) {
        element.setAttribute('content', imageUrl)
      },
    })
}

export async function onRequestGet(context) {
  const response = await context.next()
  const contentType = response.headers.get('content-type') || ''

  if (!contentType.includes('text/html')) {
    return response
  }

  return metaRewriter(context.request).transform(response)
}
