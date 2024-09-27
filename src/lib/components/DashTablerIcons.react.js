import React from 'react';
import PropTypes from 'prop-types';
import * as TablerIcons from '@tabler/icons-react';

/**
 * DashTablerIcons is a component that renders the IconAward from @tabler/icons-react.
 */
const DashTablerIcons = (props) => {
    const { size, color, stroke, strokeLinejoin, icon } = props;
    const IconComponent = TablerIcons[icon];


    return (
        <IconComponent
            size={size}
            color={color}
            stroke={stroke}
            strokeLinejoin={strokeLinejoin}
        />
    );
}

DashTablerIcons.defaultProps = {
    size: 24,
    color: 'black',
    stroke: 1,
    strokeLinejoin: 'miter'
};

DashTablerIcons.propTypes = {
    /**
     * The size of the icon (width and height).
     */
    size: PropTypes.number,

    /**
     * The color of the icon (stroke color).
     */
    color: PropTypes.string,

    /**
     * The stroke width of the icon.
     */
    stroke: PropTypes.number,

    /**
     * The stroke line join of the icon.
     */
    strokeLinejoin: PropTypes.string,

    /**
     * The name of the icon to render.
     */
    icon: PropTypes.string.isRequired
};

export default DashTablerIcons;
