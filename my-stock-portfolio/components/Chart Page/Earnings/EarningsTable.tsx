import React from 'react'

interface EarningsRecord {
  "Date": string
  "Basic Average Shares"?: number | null
  "Basic EPS"?: number | null
  "Cost Of Revenue"?: number | null
  "Diluted Average Shares"?: number | null
  "Diluted NI Availto Com Stockholders"?: number | null
  "EBIT"?: number | null
  "EBITDA"?: number | null
  "Interest Expense"?: number | null
  "Interest Income"?: number | null
  "Net Income Common Stockholders"?: number | null
  "Net Income Continuous Operations"?: number | null
  "Normalized Income"?: number | null
  "Operating Expense"?: number | null
  "Operating Revenue"?: number | null
  "Other Income Expense"?: number | null
  "Pretax Income"?: number | null
  "Reconciled Depreciation"?: number | null
  "Research And Development"?: number | null
  "Selling General And Administration"?: number | null
  "Tax Provision"?: number | null
  "Tax Rate For Calcs"?: number | null
  "Total Operating Income As Reported"?: number | null
  "dilutedEPS"?: number | null
  "grossProfit"?: number | null
  "netIncome"?: number | null
  "normalEBITDA"?: number | null
  "operatingIncome"?: number | null
  "totalExpenses"?: number | null
  "totalRevenue"?: number | null
  [key: string]: any
}

export default function EarningsTable({ earnings }: { earnings: EarningsRecord[] }) {
  if (!earnings || earnings.length === 0) return <div className="text-gray-500">No data available</div>

  const thClass = "px-2 py-1 text-left text-xs text-gray-600 dark:text-gray-300"
  const tdClass = "px-2 py-1 text-sm"

  const nf = (v: number | null | undefined) => {
    if (v === null || v === undefined) return '-'
    // show large numbers with thousands separators
    if (Math.abs(v) >= 1000) return new Intl.NumberFormat('en-US').format(v)
    return v.toString()
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-left">
        <thead className="bg-gray-100 dark:bg-zinc-800 font-medium">
          <tr>
            <th className={thClass}>Date</th>
            <th className={thClass}>Basic Avg Shares</th>
            <th className={thClass}>Basic EPS</th>
            <th className={thClass}>Diluted Avg Shares</th>
            <th className={thClass}>Diluted EPS</th>
            <th className={thClass}>Total Revenue</th>
            <th className={thClass}>Gross Profit</th>
            <th className={thClass}>Net Income</th>
            <th className={thClass}>EBIT</th>
            <th className={thClass}>EBITDA</th>
            <th className={thClass}>Operating Expense</th>
            <th className={thClass}>R&D</th>
            <th className={thClass}>SG&A</th>
            <th className={thClass}>Tax Provision</th>
            <th className={thClass}>Pretax Income</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 dark:divide-zinc-700">
          {earnings.map((row, idx) => (
            <tr key={row.date ?? idx} className="hover:bg-gray-50 dark:hover:bg-zinc-900 align-top">
              <td className={`${tdClass} font-mono`}>{row.date ? new Date(row.date).toLocaleDateString() : '-'}</td>
              <td className={tdClass}>{nf(row["Basic Average Shares"])}</td>
              <td className={tdClass}>{row["Basic EPS"] !== null && row["Basic EPS"] !== undefined ? row["Basic EPS"].toFixed(2) : '-'}</td>
              <td className={tdClass}>{nf(row["Diluted Average Shares"])}</td>
              <td className={tdClass}>{row.dilutedEPS !== null && row.dilutedEPS !== undefined ? row.dilutedEPS.toFixed(2) : '-'}</td>
              <td className={tdClass}>{nf(row.totalRevenue)}</td>
              <td className={tdClass}>{nf(row.grossProfit)}</td>
              <td className={tdClass}>{nf(row.netIncome)}</td>
              <td className={tdClass}>{nf(row.EBIT)}</td>
              <td className={tdClass}>{nf(row.EBITDA)}</td>
              <td className={tdClass}>{nf(row["Operating Expense"])}</td>
              <td className={tdClass}>{nf(row["Research And Development"])}</td>
              <td className={tdClass}>{nf(row["Selling General And Administration"])}</td>
              <td className={tdClass}>{nf(row["Tax Provision"])}</td>
              <td className={tdClass}>{nf(row["Pretax Income"])}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}