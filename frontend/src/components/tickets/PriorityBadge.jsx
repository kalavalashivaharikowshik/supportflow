import Badge from "../common/Badge";

import {
  PRIORITIES,
} from "../../constants/priorities";


const PRIORITY_VARIANTS = {
  [PRIORITIES.LOW]:
    "default",

  [PRIORITIES.MEDIUM]:
    "info",

  [PRIORITIES.HIGH]:
    "warning",

  [PRIORITIES.CRITICAL]:
    "danger",
};


const PRIORITY_LABELS = {
  [PRIORITIES.LOW]:
    "Low",

  [PRIORITIES.MEDIUM]:
    "Medium",

  [PRIORITIES.HIGH]:
    "High",

  [PRIORITIES.CRITICAL]:
    "Critical",
};


function PriorityBadge({
  priority,
}) {
  const label =
    PRIORITY_LABELS[
      priority
    ] ?? "Unknown";

  return (
    <Badge
      variant={
        PRIORITY_VARIANTS[
          priority
        ] ?? "default"
      }
    >
      {label}
    </Badge>
  );
}


export default PriorityBadge;