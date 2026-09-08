import { Panel, PanelBody, PanelHeader } from '@/components/panel'
import { seriesColor } from '@/components/series'
import { SourceDetail } from '@/components/source-card'
import { DisclosurePanel, WarningsList } from '@/components/states'
import { formatCount, formatDayShort, formatMoney } from '@/format'
import { SCAN_WARNINGS, SOURCES, sourceTrend } from './data'

export function SourcesScreen() {
  const detected = SOURCES.filter((source) => source.detected)
  const undetected = SOURCES.filter((source) => !source.detected)
  const withTokens = detected.filter((source) => source.hasTokens).length

  return (
    <div className="flex flex-col gap-3">
      <Panel>
        <PanelHeader
          eyebrow="Readers with data"
          title={`${formatCount(detected.length)} readers found logs, ${formatCount(withTokens)} of them with token counts`}
        />
        <div>
          {detected.map((source) => (
            <SourceDetail
              key={source.id}
              source={{
                id: source.id,
                label: source.label,
                path: source.path,
                clients: source.clients,
                hasTokens: source.hasTokens,
                color: seriesColor(source.slot),
                headline: source.hasTokens
                  ? formatMoney(source.cost)
                  : formatCount(source.requests),
                foot: '',
                trend: sourceTrend(source.id, source.hasTokens),
              }}
              stats={[
                { label: 'Files', value: formatCount(source.files) },
                { label: 'Sessions', value: formatCount(source.sessions) },
                { label: 'Requests', value: formatCount(source.requests) },
                {
                  label: 'Last event',
                  value: source.lastEvent ? formatDayShort(source.lastEvent) : 'none',
                },
              ]}
            />
          ))}
        </div>
      </Panel>

      {undetected.length > 0 ? (
        <DisclosurePanel
          title="Available, not detected here"
          summary={`${undetected.length} more readers ship with the tool and found nothing here: ${undetected
            .map((source) => source.id)
            .join(', ')}`}
        >
          <div className="space-y-3">
            {undetected.map((source) => (
              <div
                key={source.id}
                className="grid gap-2 border-b pb-3 last:border-b-0 last:pb-0 sm:grid-cols-[200px_minmax(0,1fr)]"
              >
                <div className="text-xs text-muted-foreground">{source.label}</div>
                <div className="min-w-0 space-y-1">
                  <div className="tabular text-[11px] break-all text-muted-foreground">
                    {source.path}
                  </div>
                  <div className="tabular text-[11px] text-muted-foreground">{source.rootHint}</div>
                </div>
              </div>
            ))}
            <p className="max-w-prose text-xs leading-relaxed text-muted-foreground">
              These readers ship with the tool but found nothing on this machine, so they stay out
              of the filter rail, the totals, and every chart. Give one a path and it appears
              everywhere on the next scan.
            </p>
          </div>
        </DisclosurePanel>
      ) : null}

      {SCAN_WARNINGS.length > 0 ? (
        <Panel>
          <PanelHeader
            eyebrow="Scan warnings"
            title={`${formatCount(SCAN_WARNINGS.length)} file or parse warnings from the last scan`}
          />
          <PanelBody>
            <WarningsList groups={[{ kind: 'other', label: 'Warnings', count: SCAN_WARNINGS.length, summary: `${SCAN_WARNINGS.length} warnings`, warnings: SCAN_WARNINGS }]} />
          </PanelBody>
        </Panel>
      ) : null}
    </div>
  )
}
