export const formatDateTime = (
  value
) => {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "—";
  }

  return new Intl.DateTimeFormat(
    undefined,
    {
      dateStyle: "medium",
      timeStyle: "short",
    }
  ).format(date);
};


export const formatRelativeTime = (
  value
) => {
  if (!value) {
    return "—";
  }

  const timestamp =
    new Date(value).getTime();

  if (Number.isNaN(timestamp)) {
    return "—";
  }

  const difference =
    timestamp - Date.now();

  const minutes = Math.round(
    difference / 60000
  );

  if (Math.abs(minutes) < 60) {
    const formatter =
      new Intl.RelativeTimeFormat(
        undefined,
        {
          numeric: "auto",
        }
      );

    return formatter.format(
      minutes,
      "minute"
    );
  }

  const hours = Math.round(
    minutes / 60
  );

  if (Math.abs(hours) < 24) {
    const formatter =
      new Intl.RelativeTimeFormat(
        undefined,
        {
          numeric: "auto",
        }
      );

    return formatter.format(
      hours,
      "hour"
    );
  }

  return formatDateTime(value);
};