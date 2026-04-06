type SourceAttributionProps = {
  sourceName: string;
  sourceUrl: string;
  licenseName: string;
  licenseUrl: string;
  attributionText: string;
};

export function SourceAttribution({
  sourceName,
  sourceUrl,
  licenseName,
  licenseUrl,
  attributionText,
}: SourceAttributionProps) {
  return (
    <div className="rounded-xl border p-4 space-y-2 text-sm bg-white">
      <div>
        <span className="font-semibold">Source: </span>
        <a
          href={sourceUrl}
          target="_blank"
          rel="noreferrer"
          className="underline"
        >
          {sourceName}
        </a>
      </div>

      <div>
        <span className="font-semibold">License: </span>
        <a
          href={licenseUrl}
          target="_blank"
          rel="noreferrer"
          className="underline"
        >
          {licenseName}
        </a>
      </div>

      <div>
        <span className="font-semibold">Attribution: </span>
        <span>{attributionText}</span>
      </div>
    </div>
  );
}
