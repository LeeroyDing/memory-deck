import React from 'react';

export const ServerAPI = {
  callPluginMethod: jest.fn(),
};

export const Router = {
  Navigate: jest.fn(),
};

export const gamepadDialogClasses = {
  Field: 'Field',
  WithBottomSeparatorStandard: 'WithBottomSeparatorStandard',
  FieldLabelRow: 'FieldLabelRow',
  FieldLabel: 'FieldLabel',
  FieldChildren: 'FieldChildren',
};

export const joinClassNames = (...args: string[]) => args.join(' ');

export const DialogButton = ({ children, onClick }: any) => (
  <button onClick={onClick}>{children}</button>
);

export const Focusable = ({ children, style, className }: any) => (
  <div style={style} className={className}>{children}</div>
);

export const PanelSectionRow = ({ children }: any) => <div>{children}</div>;
