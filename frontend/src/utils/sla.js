export const getSlaState = ({
  isBreached,
  isAtRisk,
}) => {
  if (isBreached) {
    return "BREACHED";
  }

  if (isAtRisk) {
    return "AT_RISK";
  }

  return "HEALTHY";
};


export const formatRemainingTime = (
  seconds
) => {
  if (
    seconds === null ||
    seconds === undefined
  ) {
    return "—";
  }

  if (seconds <= 0) {
    return "SLA breached";
  }

  const hours = Math.floor(
    seconds / 3600
  );

  const minutes = Math.floor(
    (seconds % 3600) / 60
  );

  if (hours > 0) {
    return `${hours}h ${minutes}m remaining`;
  }

  return `${minutes}m remaining`;
};