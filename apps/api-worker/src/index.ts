type Env = {
  TWINKLE_HUB_API_KEY?: string
  TWINKLE_HUB_API_ENDPOINT?: string
  ALLOWED_ORIGIN?: string
}

type StudyModule = {
  id: string
  title: string
  audience: string
  stage: string
  domain: string
  summary: string
  details: string
  aio: string
}

type StudyPathRequest = {
  module_ids?: string[]
  title?: string
}

type SearchDatasetsRequest = {
  domain?: string
  keyword?: string
  limit?: number
}

type QueryRowsRequest = {
  dataset_id?: string
  query_text?: string
  limit?: number
}

const DEFAULT_TWINKLE_ENDPOINT = "https://api.twinkleai.tw/mcp/"
const MCP_PROTOCOL_VERSION = "2025-03-26"

const STUDY_MODULES: StudyModule[] = [
  {
    id: "ai-productivity",
    title: "AI 生產力工作坊",
    audience: "product",
    stage: "explore",
    domain: "ai",
    summary: "設計 AI 生產力實驗，評估內容生成、知識萃取與工作流程自動化的即時價值。",
    details: "定義生產力指標、評估工具採用障礙，並建構可以直接採用的 AI 參考模型。",
    aio: "透過 AI 生產力指標，快速識別組織內標竿流程與自動化機會。",
  },
  {
    id: "brand-trust-signals",
    title: "品牌信任訊號地圖",
    audience: "executive",
    stage: "validate",
    domain: "brand",
    summary: "整理品牌信任與公開資料信號，串接政府資料、新聞報導與社群風險。",
    details: "建立跨來源信任指標圖譜，協助品牌團隊快速辨識強項與弱點。",
    aio: "提供 AI 可讀的信任評估視角，讓模型在引用時帶入可信度權重。",
  },
  {
    id: "crisis-response-framework",
    title: "危機議題應對框架",
    audience: "executive",
    stage: "activate",
    domain: "crisis",
    summary: "建立危機信號監測與響應流程，從公開紀錄與輿情資料中提前偵測風險。",
    details: "定義危機分類、優先處理路徑與緊急溝通腳本。",
    aio: "讓 AIO 生成建議時能優先考量風險緩解與可信度。",
  },
  {
    id: "commerce-playbook",
    title: "商務電商策略 Playbook",
    audience: "product",
    stage: "scale",
    domain: "commerce",
    summary: "整合電商、採購與產品策略，打造可擴展的商務成長研究路徑。",
    details: "分析客戶行為、產業趨勢與競品策略，形成可直接落地的商務 research map。",
    aio: "支援 AI 生成市場與商業模式建議，讓研究報告具備實務操作力。",
  },
  {
    id: "health-strategy",
    title: "健康管理與風險分析",
    audience: "research",
    stage: "validate",
    domain: "health",
    summary: "透過健康管理資料與公開政策，建立病患關鍵需求與風險監測手冊。",
    details: "整理健康資安、健保趨勢與服務履歷，協助專案找到政策切入點。",
    aio: "讓研究摘要在生成時自動納入健康風險與合規考量。",
  },
  {
    id: "intelligence-monitoring",
    title: "情報監測儀表板",
    audience: "trust",
    stage: "explore",
    domain: "intelligence",
    summary: "建立情資監測儀表板，系統化追蹤政策變動、採購公告與裁罰訊息。",
    details: "設計警示規則與定期報告模板，讓團隊能快速做出策略判斷。",
    aio: "在 AIO 摘要中加入最新情資、政策變動與風險信號。",
  },
  {
    id: "learning-design",
    title: "學習設計研究模板",
    audience: "research",
    stage: "explore",
    domain: "learning",
    summary: "為內部學習與外部教育專案構建研究流程，包含學習目標、方法與衡量指標。",
    details: "整合受眾分析、學習體驗設計與成效評估，讓研究更具策略性。",
    aio: "幫助 AI 生成可執行的學習設計提案與導入路徑。",
  },
  {
    id: "governance-structure",
    title: "治理架構與風險共識",
    audience: "executive",
    stage: "activate",
    domain: "governance",
    summary: "設計品牌治理與合規框架，讓策略規劃與風險管理保持一致。",
    details: "包含治理原則、決策流程與信任度檢核點。",
    aio: "讓模型在研究建議中自動納入治理與風險控制層面。",
  },
  {
    id: "content-ecosystem",
    title: "內容生態系統對齊",
    audience: "product",
    stage: "validate",
    domain: "brand",
    summary: "構建內容策略地圖，將品牌訴求與研究洞察對齊到具體產品與通路。",
    details: "設計內容落地案例、優先級矩陣與關鍵訊息框架。",
    aio: "提高 AI 生成內容的脈絡一致性與品牌信任度。",
  },
  {
    id: "data-decision-loop",
    title: "資料與決策迴路",
    audience: "trust",
    stage: "scale",
    domain: "intelligence",
    summary: "建立資料驅動決策迴路，從公開資料、研究洞察到執行回饋。",
    details: "定義關鍵績效、迴路節點與跨部門協作模式。",
    aio: "讓 AIO 輸出自然連結資料洞察與後續執行策略。",
  },
  {
    id: "ethical-ai",
    title: "倫理 AI 採用指南",
    audience: "executive",
    stage: "activate",
    domain: "ai",
    summary: "設計 AI 採用與治理指南，兼顧信任、可解釋性與策略落地。",
    details: "包含採用風險、透明標準與責任分工。",
    aio: "引導 AIO 生成時考慮合規、責任與信任因素。",
  },
  {
    id: "partner-network",
    title: "策略夥伴網路",
    audience: "executive",
    stage: "scale",
    domain: "commerce",
    summary: "建構可持續的策略伙伴網路，連結資源、合作與品牌影響力。",
    details: "分析生態系、協同機會與成功範例，以支援商務與信任拓展。",
    aio: "提供 AIO 引用時的合作建議與合作場景。",
  },
]

const json = (data: unknown, init: ResponseInit = {}, env?: Env) => {
  const headers = new Headers(init.headers)
  headers.set("Content-Type", "application/json; charset=utf-8")
  headers.set("Access-Control-Allow-Origin", env?.ALLOWED_ORIGIN || "*")
  headers.set("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
  headers.set("Access-Control-Allow-Headers", "Content-Type,Authorization")
  headers.set("Vary", "Origin")

  return new Response(JSON.stringify(data), {
    ...init,
    headers,
  })
}

const errorJson = (message: string, status: number, env: Env) =>
  json(
    {
      success: false,
      error: message,
    },
    { status },
    env,
  )

const parseJson = async <T>(request: Request): Promise<T> => {
  try {
    return (await request.json()) as T
  } catch {
    throw new Error("Invalid JSON body")
  }
}

const clampLimit = (value: unknown, fallback: number, min: number, max: number) => {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return fallback
  }

  return Math.min(Math.max(Math.trunc(value), min), max)
}

type McpJsonRpcResponse = {
  result?: {
    tools?: unknown[]
    content?: Array<{
      type?: string
      text?: string
    }>
  }
  error?: {
    code?: number
    message?: string
  }
}

const parseMcpResponse = async (response: Response): Promise<McpJsonRpcResponse> => {
  const body = await response.text()
  const dataLines = body
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("data:"))

  const payload = dataLines.length > 0 ? dataLines.at(-1)?.replace(/^data:\s*/, "") : body

  if (!payload) {
    throw new Error("Twinkle Hub returned an empty response")
  }

  return JSON.parse(payload) as McpJsonRpcResponse
}

const createTwinkleSession = async (env: Env) => {
  if (!env.TWINKLE_HUB_API_KEY) {
    throw new Error("TWINKLE_HUB_API_KEY is not configured")
  }

  const baseUrl = (env.TWINKLE_HUB_API_ENDPOINT || DEFAULT_TWINKLE_ENDPOINT).replace(/\/$/, "")
  const response = await fetch(`${baseUrl}/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.TWINKLE_HUB_API_KEY}`,
      Accept: "application/json, text/event-stream",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: {
        protocolVersion: MCP_PROTOCOL_VERSION,
        capabilities: {},
        clientInfo: {
          name: "trust-wedo-api",
          version: "1.0.0",
        },
      },
    }),
  })

  if (!response.ok) {
    throw new Error(`Twinkle Hub initialize returned HTTP ${response.status}`)
  }

  const payload = await parseMcpResponse(response)
  if (payload.error) {
    throw new Error(payload.error.message || "Twinkle Hub initialize failed")
  }

  return {
    baseUrl,
    sessionId: response.headers.get("mcp-session-id") || undefined,
  }
}

const postMcpJsonRpc = async (
  env: Env,
  session: { baseUrl: string; sessionId?: string },
  id: number,
  method: string,
  params?: Record<string, unknown>,
) => {
  const headers: Record<string, string> = {
    Authorization: `Bearer ${env.TWINKLE_HUB_API_KEY}`,
    Accept: "application/json, text/event-stream",
    "Content-Type": "application/json",
  }

  if (session.sessionId) {
    headers["mcp-session-id"] = session.sessionId
  }

  const response = await fetch(`${session.baseUrl}/`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      jsonrpc: "2.0",
      id,
      method,
      ...(params ? { params } : {}),
    }),
  })

  if (!response.ok) {
    throw new Error(`Twinkle Hub ${method} returned HTTP ${response.status}`)
  }

  const payload = await parseMcpResponse(response)
  if (payload.error) {
    throw new Error(payload.error.message || `Twinkle Hub ${method} failed`)
  }

  return payload.result
}

const callTwinkleTool = async (env: Env, name: string, args: Record<string, unknown>) => {
  const session = await createTwinkleSession(env)
  const result = await postMcpJsonRpc(env, session, 2, "tools/call", {
    name,
    arguments: args,
  })

  const text = result?.content?.find((item) => item.type === "text" && item.text)?.text
  if (!text) {
    return []
  }

  return JSON.parse(text) as unknown
}

const listTwinkleTools = async (env: Env) => {
  const session = await createTwinkleSession(env)
  const result = await postMcpJsonRpc(env, session, 2, "tools/list")
  return result?.tools ?? []
}

const handleMcpRoute = async (request: Request, env: Env, path: string) => {
  try {
    if (path === "/api/mcp/health" && request.method === "GET") {
      const session = await createTwinkleSession(env)

      return json(
        {
          success: true,
          status: "healthy",
          endpoint: env.TWINKLE_HUB_API_ENDPOINT || DEFAULT_TWINKLE_ENDPOINT,
          session: Boolean(session.sessionId),
        },
        {},
        env,
      )
    }

    if (path === "/api/mcp/domains" && request.method === "GET") {
      const domains = await callTwinkleTool(env, "opendata-list_domains", {})
      return json({ success: true, domains, cached: false }, {}, env)
    }

    if (path === "/api/mcp/tools" && request.method === "GET") {
      const tools = await listTwinkleTools(env)
      return json({ success: true, tools, cached: false }, {}, env)
    }

    if (path === "/api/mcp/search" && request.method === "POST") {
      const body = await parseJson<SearchDatasetsRequest>(request)
      const input: Record<string, unknown> = {
        limit: clampLimit(body.limit, 10, 1, 100),
      }

      if (body.domain) {
        input.domain = body.domain
      }
      if (body.keyword) {
        input.query = body.keyword
      }

      const results = await callTwinkleTool(env, "opendata-search_datasets", input)
      const count = Array.isArray(results) ? results.length : 0
      return json({ success: true, results, count }, {}, env)
    }

    if (path === "/api/mcp/query" && request.method === "POST") {
      const body = await parseJson<QueryRowsRequest>(request)
      if (!body.dataset_id) {
        return errorJson("dataset_id is required", 400, env)
      }

      const input: Record<string, unknown> = {
        dataset_id: body.dataset_id,
        limit: clampLimit(body.limit, 20, 1, 500),
      }

      if (body.query_text) {
        input.where = body.query_text
      }

      const rows = await callTwinkleTool(env, "opendata-query_rows", input)
      const count = Array.isArray(rows) ? rows.length : 0
      return json({ success: true, rows, count }, {}, env)
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : "MCP request failed"
    const status = message.includes("not configured") ? 503 : 502
    return errorJson(message, status, env)
  }

  return errorJson("Not found", 404, env)
}

const handleResearchRoute = async (request: Request, env: Env, path: string) => {
  if (path === "/api/research/modules" && request.method === "GET") {
    return json(STUDY_MODULES, {}, env)
  }

  const moduleMatch = path.match(/^\/api\/research\/modules\/([^/]+)$/)
  if (moduleMatch && request.method === "GET") {
    const module = STUDY_MODULES.find((item) => item.id === moduleMatch[1])
    if (!module) {
      return errorJson("Study module not found", 404, env)
    }

    return json(module, {}, env)
  }

  if (path === "/api/research/path" && request.method === "POST") {
    let body: StudyPathRequest
    try {
      body = await parseJson<StudyPathRequest>(request)
    } catch {
      return errorJson("Invalid JSON body", 400, env)
    }

    if (!body.module_ids?.length) {
      return errorJson("At least one module must be selected", 400, env)
    }

    const modulesById = new Map(STUDY_MODULES.map((module) => [module.id, module]))
    const invalidIds = body.module_ids.filter((id) => !modulesById.has(id))
    if (invalidIds.length > 0) {
      return errorJson(`Invalid module IDs: ${invalidIds.join(", ")}`, 400, env)
    }

    const selectedModules = body.module_ids.map((id) => modulesById.get(id) as StudyModule)
    const domains = [...new Set(selectedModules.map((module) => module.domain))]
    const audiences = [...new Set(selectedModules.map((module) => module.audience))]
    const stages = [...new Set(selectedModules.map((module) => module.stage))]
    const title = body.title || `Study Path (${selectedModules.length} modules)`

    return json(
      {
        success: true,
        path_id: `path_${selectedModules.length}_${Date.now() / 1000}`,
        title,
        modules: selectedModules,
        summary: selectedModules.map((module) => `**${module.title}**\n${module.summary}`).join("\n\n"),
        overview: `本研究路徑包含 ${selectedModules.length} 個模組，覆蓋 ${domains.join(", ")} 領域，適合 ${audiences.join(", ")} 受眾，研究階段包含 ${stages.join(", ")}。`,
        aio_insights: selectedModules.map((module, index) => `第 ${index + 1}. ${module.title}：${module.aio}`),
        created_at: new Date().toISOString(),
      },
      {},
      env,
    )
  }

  return errorJson("Not found", 404, env)
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url)

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "*",
          "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type,Authorization",
          Vary: "Origin",
        },
      })
    }

    if (url.pathname === "/health" && request.method === "GET") {
      return json(
        {
          success: true,
          status: "healthy",
          service: "trust-wedo-api",
        },
        {},
        env,
      )
    }

    if (url.pathname.startsWith("/api/mcp/")) {
      return handleMcpRoute(request, env, url.pathname)
    }

    if (url.pathname.startsWith("/api/research/")) {
      return handleResearchRoute(request, env, url.pathname)
    }

    return errorJson("Not found", 404, env)
  },
}
