import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

type BookstoreCategory =
  | '大型連鎖書店'
  | '獨立特色書店'
  | '經銷書店'
  | '書香取書門市'
  | '公立圖書館'
  | '大學圖書館'
  | '國家圖書館'

type BookstoreLocation = {
  id: string
  name: string
  chain: string
  category: BookstoreCategory
  city: string
  district: string
  address: string
  phone: string
  description: string
  image: string
  latitude: string
  longitude: string
  openTime: string
  detailUrl: string
  mapsUrl: string
  sourceName: string
  sourceUrl: string
  tags: string[]
  priority: number
}

type BookstoreDataset = {
  metadata: {
    generatedAt: string
    totalCount: number
    countsByCategory: Partial<Record<BookstoreCategory, number>>
  }
  items: BookstoreLocation[]
}

declare global {
  interface Window {
    L?: any
  }
}

const categories: Array<BookstoreCategory | '全部'> = [
  '全部',
  '大型連鎖書店',
  '獨立特色書店',
  '經銷書店',
  '書香取書門市',
  '公立圖書館',
  '大學圖書館',
  '國家圖書館',
]

const categoryStyle: Record<string, { dot: string; label: string }> = {
  大型連鎖書店: { dot: '#345f7d', label: '連鎖' },
  獨立特色書店: { dot: '#b77738', label: '獨立' },
  經銷書店: { dot: '#6f5a45', label: '經銷' },
  書香取書門市: { dot: '#2f7d5b', label: '書香' },
  公立圖書館: { dot: '#667761', label: '圖書館' },
  大學圖書館: { dot: '#6d5f8e', label: '大學' },
  國家圖書館: { dot: '#8a4b52', label: '國圖' },
}

const defaultCategoryStyle = { dot: '#8f6a45', label: '書店' }

function normalize(value: string) {
  return value.replace(/臺/g, '台').toLowerCase().trim()
}

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean))).sort((a, b) => a.localeCompare(b, 'zh-Hant'))
}

function formatDate(value: string) {
  if (!value) return ''
  return new Date(value).toLocaleDateString('zh-TW')
}

function firstPhone(value: string) {
  return value.match(/[+()#\-\d\s]{7,}/)?.[0]?.replace(/[^\d+]/g, '') ?? ''
}

function hasGeo(item: BookstoreLocation) {
  return Boolean(Number(item.latitude) && Number(item.longitude))
}

function openMaps(item: BookstoreLocation) {
  const query = encodeURIComponent(`${item.name} ${item.address}`)
  window.open(item.mapsUrl || `https://www.google.com/maps/search/?api=1&query=${query}`, '_blank', 'noopener,noreferrer')
}

function filterItems(
  items: BookstoreLocation[],
  query: string,
  category: BookstoreCategory | '全部',
  city: string,
  chain: string,
) {
  const q = normalize(query)
  const normalizedCity = city === '全部' ? '' : normalize(city)
  const normalizedChain = chain === '全部' ? '' : normalize(chain)

  return items
    .filter((item) => {
      const haystack = normalize([
        item.name,
        item.chain,
        item.category,
        item.city,
        item.district,
        item.address,
        item.phone,
        item.description,
        item.openTime,
        ...item.tags,
      ].join(' '))

      return (
        (!q || haystack.includes(q)) &&
        (category === '全部' || item.category === category) &&
        (!normalizedCity || normalize(item.city) === normalizedCity) &&
        (!normalizedChain || normalize(item.chain) === normalizedChain)
      )
    })
    .sort((a, b) => a.priority - b.priority || a.city.localeCompare(b.city, 'zh-Hant') || a.name.localeCompare(b.name, 'zh-Hant'))
}

export default function BookstoreMap() {
  const [dataset, setDataset] = useState<BookstoreDataset | null>(null)
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState<BookstoreCategory | '全部'>('全部')
  const [city, setCity] = useState('全部')
  const [chain, setChain] = useState('全部')
  const [mode, setMode] = useState<'list' | 'map'>('list')
  const [selected, setSelected] = useState<BookstoreLocation | null>(null)
  const [leafletLoaded, setLeafletLoaded] = useState(false)
  const mapRef = useRef<any>(null)
  const markerRefs = useRef<any[]>([])

  useEffect(() => {
    fetch('/bookstores/bookstores.json')
      .then((response) => {
        if (!response.ok) throw new Error('bookstores.json load failed')
        return response.json() as Promise<BookstoreDataset>
      })
      .then((data) => {
        setDataset(data)
        setSelected(data.items.find(hasGeo) ?? data.items[0] ?? null)
      })
      .catch((error) => console.error('[BookstoreMap] failed to load dataset', error))
  }, [])

  useEffect(() => {
    if (window.L) {
      setLeafletLoaded(true)
      return
    }

    if (!document.getElementById('book-wedo-leaflet-css')) {
      const link = document.createElement('link')
      link.id = 'book-wedo-leaflet-css'
      link.rel = 'stylesheet'
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
      document.head.appendChild(link)
    }

    if (!document.getElementById('book-wedo-leaflet-js')) {
      const script = document.createElement('script')
      script.id = 'book-wedo-leaflet-js'
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
      script.onload = () => setLeafletLoaded(true)
      document.head.appendChild(script)
    }
  }, [])

  const allItems = dataset?.items ?? []
  const items = useMemo(
    () => filterItems(allItems, query, category, city, chain),
    [allItems, query, category, city, chain],
  )
  const visibleCards = items.slice(0, 80)
  const cityOptions = useMemo(() => ['全部', ...unique(allItems.map((item) => item.city))], [allItems])
  const chainOptions = useMemo(() => ['全部', ...unique(allItems.map((item) => item.chain))], [allItems])
  const counts = dataset?.metadata.countsByCategory ?? {}

  useEffect(() => {
    if (!selected || !items.some((item) => item.id === selected.id)) {
      setSelected(items.find(hasGeo) ?? items[0] ?? null)
    }
  }, [items, selected])

  useEffect(() => {
    if (!leafletLoaded || mode !== 'map' || mapRef.current) return

    const map = window.L.map('trust-wedo-bookstore-map', {
      zoomControl: false,
      attributionControl: false,
    }).setView([23.75, 120.96], 7)

    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
    }).addTo(map)
    window.L.control.zoom({ position: 'bottomright' }).addTo(map)
    mapRef.current = map

    return () => {
      markerRefs.current.forEach((marker) => marker.remove())
      markerRefs.current = []
      map.remove()
      mapRef.current = null
    }
  }, [leafletLoaded, mode])

  useEffect(() => {
    if (!mapRef.current || mode !== 'map') return
    const map = mapRef.current
    const geoItems = items.filter(hasGeo).slice(0, 300)

    markerRefs.current.forEach((marker) => marker.remove())
    markerRefs.current = []

    if (!geoItems.length) return

    const bounds = window.L.latLngBounds()
    geoItems.forEach((item) => {
      const latitude = Number(item.latitude)
      const longitude = Number(item.longitude)
      const style = categoryStyle[item.category] ?? defaultCategoryStyle
      const marker = window.L.marker([latitude, longitude], {
        icon: window.L.divIcon({
          className: 'trust-bookstore-marker',
          html: `<span style="background:${style.dot}"></span>`,
          iconSize: [20, 20],
          iconAnchor: [10, 10],
        }),
      }).addTo(map)

      marker.on('click', () => {
        setSelected(item)
        map.flyTo([latitude, longitude], 15, { duration: 0.45 })
      })
      markerRefs.current.push(marker)
      bounds.extend([latitude, longitude])
    })

    map.fitBounds(bounds, { padding: [36, 36], maxZoom: 14 })
  }, [items, leafletLoaded, mode])

  return (
    <main className="min-h-screen bg-[#1f2c25] text-[#24322b]">
      <style>{`
        .trust-bookstore-marker {
          background: transparent;
          border: 0;
        }
        .trust-bookstore-marker span {
          display: block;
          width: 18px;
          height: 18px;
          border: 3px solid white;
          border-radius: 999px;
          box-shadow: 0 8px 18px rgba(31, 44, 37, 0.28);
        }
      `}</style>

      <div className="mx-auto flex min-h-[100dvh] w-full max-w-md flex-col overflow-hidden bg-[#f7f1e8] shadow-2xl">
        <header className="z-20 flex-shrink-0 rounded-b-[28px] bg-[#fffaf1] px-4 pb-4 pt-5 shadow-[0_12px_34px_rgba(58,44,30,0.14)]">
          <div className="mb-4 flex items-start justify-between gap-3">
            <div>
              <p className="text-[11px] font-black tracking-[0.16em] text-[#a06f36]">TRUST WEDO × BOOK WEDO</p>
              <h1 className="mt-1 text-[24px] font-black leading-tight text-[#24322b]">實體書店地圖</h1>
              <p className="mt-1 text-xs font-semibold text-[#7d705f]">
                {(dataset?.metadata.totalCount ?? 0).toLocaleString()} 筆據點 · {formatDate(dataset?.metadata.generatedAt ?? '')}
              </p>
            </div>
            <Link
              to="/"
              className="grid h-14 w-14 flex-none place-items-center rounded-full bg-[#e7efe6] text-xl font-black text-[#2f684f]"
              aria-label="回到 Trust WEDO"
            >
              TW
            </Link>
          </div>

          <label className="flex h-12 items-center gap-3 rounded-full border border-[#dfd3c1] bg-[#fbf7ef] px-4">
            <span className="text-xl text-[#8f8373]">⌕</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="搜尋店名、路名、城市、類別"
              className="min-w-0 flex-1 bg-transparent text-base font-bold text-[#24322b] outline-none placeholder:text-[#9ca3af]"
            />
          </label>

          <div className="mt-4 flex gap-2 overflow-x-auto pb-1">
            {categories.map((item) => {
              const active = item === category
              return (
                <button
                  key={item}
                  type="button"
                  onClick={() => setCategory(item)}
                  className={`h-10 flex-none rounded-full border px-4 text-sm font-black transition ${
                    active
                      ? 'border-[#2f684f] bg-[#2f684f] text-white'
                      : 'border-[#dfd3c1] bg-white text-[#4c5a51]'
                  }`}
                >
                  {item}
                </button>
              )
            })}
          </div>

          <div className="mt-4 grid grid-cols-2 gap-3">
            <FilterSelect label="地區" value={city} onChange={setCity} options={cityOptions} />
            <FilterSelect label="品牌" value={chain} onChange={setChain} options={chainOptions} />
          </div>
        </header>

        <section className="relative min-h-0 flex-1 overflow-y-auto pb-28">
          {mode === 'list' ? (
            <div className="px-4 py-6">
              <div className="mb-5 flex items-end justify-between gap-3">
                <div>
                  <h2 className="text-2xl font-black">{items.length.toLocaleString()} 個結果</h2>
                  <p className="mt-1 text-sm font-bold text-[#766b5c]">全台閱讀據點</p>
                </div>
              </div>

              <div className="mb-6 grid grid-cols-4 gap-1.5">
                <MiniStat label="連鎖" value={counts['大型連鎖書店'] ?? 0} />
                <MiniStat label="獨立" value={counts['獨立特色書店'] ?? 0} />
                <MiniStat label="經銷" value={counts['經銷書店'] ?? 0} />
                <MiniStat label="書香" value={counts['書香取書門市'] ?? 0} />
              </div>

              <div className="grid gap-4">
                {visibleCards.map((item) => (
                  <BookstoreCard key={item.id} item={item} onOpenMap={() => openMaps(item)} />
                ))}
              </div>
            </div>
          ) : (
            <div className="relative h-full min-h-[620px]">
              <div id="trust-wedo-bookstore-map" className="absolute inset-0" />
              <div className="absolute right-4 top-5 z-[500] rounded-3xl bg-white/92 p-4 shadow-xl">
                {Object.entries(categoryStyle).slice(0, 5).map(([name, style]) => (
                  <div key={name} className="mb-2 flex items-center gap-3 last:mb-0">
                    <span className="h-3 w-3 rounded-full" style={{ background: style.dot }} />
                    <span className="text-sm font-black">{style.label}</span>
                  </div>
                ))}
              </div>
              {selected && <MapSheet item={selected} onClose={() => setSelected(null)} />}
            </div>
          )}
        </section>

        <nav className="fixed bottom-0 left-1/2 z-[600] grid w-full max-w-md -translate-x-1/2 grid-cols-2 gap-2 border-t border-[#e0d2be] bg-white/95 p-4 backdrop-blur">
          <button
            type="button"
            onClick={() => setMode('list')}
            className={`h-16 rounded-[24px] text-sm font-black ${mode === 'list' ? 'bg-[#e7efe6] text-[#2f684f]' : 'text-[#8a7f70]'}`}
          >
            <span className="block text-xl">☷</span>
            列表模式
          </button>
          <button
            type="button"
            onClick={() => setMode('map')}
            className={`h-16 rounded-[24px] text-sm font-black ${mode === 'map' ? 'bg-[#e7efe6] text-[#2f684f]' : 'text-[#8a7f70]'}`}
          >
            <span className="block text-xl">◇</span>
            地圖模式
          </button>
        </nav>
      </div>
    </main>
  )
}

function FilterSelect({
  label,
  value,
  onChange,
  options,
}: {
  label: string
  value: string
  onChange: (value: string) => void
  options: string[]
}) {
  return (
    <label>
      <span className="mb-2 block text-xs font-black text-[#7d705f]">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="h-11 w-full appearance-none rounded-2xl border border-[#dfd3c1] bg-[#f8f3eb] px-3 text-sm font-bold text-[#24322b] outline-none focus:border-[#2f684f] focus:ring-4 focus:ring-[#2f684f]/10"
      >
        {options.map((option) => <option key={option}>{option}</option>)}
      </select>
    </label>
  )
}

function MiniStat({ label, value }: { label: string; value: number }) {
  return (
    <div className="min-w-0 rounded-2xl border border-[#e3d6c2] bg-[#fffaf1] p-2.5">
      <strong className="block truncate text-base leading-none">{value.toLocaleString()}</strong>
      <span className="mt-1 block truncate text-[10px] font-bold text-[#7d705f]">{label}</span>
    </div>
  )
}

function BookstoreCard({ item, onOpenMap }: { item: BookstoreLocation; onOpenMap: () => void }) {
  const phone = firstPhone(item.phone)
  const style = categoryStyle[item.category] ?? defaultCategoryStyle

  return (
    <article className="overflow-hidden rounded-[24px] border border-[#e2d5c1] bg-white shadow-sm active:scale-[0.99]">
      <button type="button" onClick={onOpenMap} className="relative block h-36 w-full overflow-hidden text-left">
        {item.image ? (
          <img src={item.image} alt={item.name} loading="lazy" className="h-full w-full object-cover" />
        ) : (
          <div className="grid h-full place-items-center bg-gradient-to-br from-[#e8dfcf] to-[#cfdccf] text-2xl font-black text-[#2f684f]">
            {style.label}
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/10 to-transparent" />
        <div className="absolute bottom-3 left-3 flex gap-2">
          <span className="rounded-full px-2.5 py-1 text-xs font-black text-white" style={{ background: style.dot }}>{item.category}</span>
          <span className="rounded-full bg-white/90 px-2.5 py-1 text-xs font-black text-[#24322b]">{item.city}</span>
        </div>
      </button>

      <div className="p-4">
        <button type="button" onClick={onOpenMap} className="block text-left text-lg font-black leading-tight text-[#24322b]">
          {item.name}
        </button>
        <p className="mt-1 line-clamp-2 text-sm leading-relaxed text-[#685d4e]">{item.description || item.chain}</p>

        <button type="button" onClick={onOpenMap} className="mt-3 flex w-full items-start gap-2 rounded-2xl bg-[#f8f3eb] p-3 text-left text-sm text-[#4f5a52]">
          <span className="mt-0.5 flex-none text-[#345f7d]">⌖</span>
          <span>{item.address}</span>
        </button>

        <div className="mt-3 flex gap-2">
          <button type="button" onClick={onOpenMap} className="flex h-10 flex-1 items-center justify-center gap-1 rounded-2xl bg-[#2f684f] text-sm font-black text-white">
            ↗ 導航
          </button>
          {phone && (
            <a href={`tel:${phone}`} className="grid h-10 w-12 place-items-center rounded-2xl bg-[#e7efe6] text-lg text-[#2f684f]">
              ☎
            </a>
          )}
        </div>
      </div>
    </article>
  )
}

function MapSheet({ item, onClose }: { item: BookstoreLocation; onClose: () => void }) {
  const style = categoryStyle[item.category] ?? defaultCategoryStyle
  const phone = firstPhone(item.phone)

  return (
    <div className="absolute bottom-8 left-4 right-4 z-[520] rounded-[28px] bg-white p-4 shadow-2xl">
      <button
        type="button"
        onClick={onClose}
        className="absolute right-4 top-4 grid h-10 w-10 place-items-center rounded-full bg-[#6f6f6f] text-2xl font-light text-white"
      >
        ×
      </button>

      <div className="flex gap-4 pr-10">
        {item.image ? (
          <img src={item.image} alt={item.name} className="h-24 w-24 flex-none rounded-[24px] object-cover" />
        ) : (
          <div className="grid h-24 w-24 flex-none place-items-center rounded-[24px] bg-[#e8dfcf] font-black text-[#2f684f]">
            {style.label}
          </div>
        )}

        <div className="min-w-0 flex-1">
          <p className="text-xs font-black text-[#a06f36]">{item.category}</p>
          <h3 className="mt-1 line-clamp-2 text-xl font-black leading-tight">{item.name}</h3>
          <p className="mt-2 line-clamp-2 text-sm font-semibold text-[#6d6254]">{item.address}</p>

          <div className="mt-4 flex gap-2">
            <button type="button" onClick={() => openMaps(item)} className="h-11 flex-1 rounded-2xl bg-[#345f7d] px-4 text-sm font-black text-white">
              Google Maps
            </button>
            {phone && (
              <a href={`tel:${phone}`} className="grid h-11 w-14 place-items-center rounded-2xl bg-[#e7efe6] text-lg text-[#2f684f]">
                ☎
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
