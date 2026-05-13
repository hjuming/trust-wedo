export interface EntityCheckResult {
  companyInfo: {
    name: string
    taxId: string
    status: string
    address?: string
    registerAuthority?: string
    capitalAmount?: number
    responsibleName?: string
  }
  validation: {
    taxIdValid: boolean
    rule?: string
  }
  riskSignals: Array<{
    title: string
    description: string
    severity: 'low' | 'medium' | 'high' | 'critical'
    source: string
    date?: string
  }>
  websiteAnalysis?: {
    url: string
    trustScore: number
    aiReadability: string
    lastAnalyzed?: string
  }
  dataSources: Array<{
    name: string
    type: string
    lastUpdated: string
    url?: string
  }>
  generatedAt: string
}