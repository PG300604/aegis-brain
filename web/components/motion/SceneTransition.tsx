"use client";

import React from "react";
import { VerticalRippleCurtain } from "./VerticalRippleCurtain";

interface SceneTransitionProps {
  fromAct?: string;
  toAct?: string;
  badge?: string;
  dark?: boolean;
}

export function SceneTransition({
  fromAct = "FEATURE 01",
  toAct = "FEATURE 02",
  badge = "A DIMENSIONAL SHIFT TRANSPIRES • THE MEMORY INDEX RECONVERGES WITH SUB-SECOND WAL SPEED",
  dark = true,
}: SceneTransitionProps) {
  return (
    <VerticalRippleCurtain
      fromAct={fromAct}
      toAct={toAct}
      narration={badge}
    />
  );
}
